# a snipet of deeplearning training with ignite.


def training(model, loss, train_loader, test_loader, n_epochs, device, model_dst_dir):
    optim = torch.optim.SGD(model.parameters(), lr=0.1)
    scheduler = CyclicLR(optim, base_lr=1e-5, max_lr=1e-2)
    trainer = create_supervised_trainer(model, optim, loss, device=device)
    evaluator = create_supervised_evaluator(
        model, metrics={
            'acc': CategoricalAccuracy(),
            'loss': Loss(loss)
        },
        device=device)

    exp_name = 'training'
    with hyper_dash_manager(exp_name, debug=True) as exp:
        timer = Timer(average=False)
        timer.attach(trainer, start=Events.EPOCH_STARTED, pause=Events.EPOCH_COMPLETED)

        model_handler = ModelCheckpoint(
            model_dst_dir, exp_name,
            # score_function=lambda engine: engine.state.metrics['acc'],
            # score_name='acc',
            save_interval=5,
            require_empty=False)
        evaluator.add_event_handler(Events.EPOCH_COMPLETED, model_handler, {'deep_unet': model})

        @trainer.on(Events.EPOCH_STARTED)
        def log_epoch(engine: Engine):
            Functions.PrintFunc.success(f"{engine.state.epoch} epoch start.")
            setattr(engine.state, 'train_loss', 0)

        @trainer.on(Events.ITERATION_COMPLETED)
        def record_loss(engine: Engine):
            engine.state.train_loss += engine.state.output

        @trainer.on(Events.ITERATION_COMPLETED)
        def update_clr(engine: Engine):
            scheduler.batch_step()

        @trainer.on(Events.EPOCH_COMPLETED)
        def test_metrics(engine: Engine):
            evaluator.run(test_loader)
            metrics = evaluator.state.metrics

            exp.metric('train_loss', engine.state.train_loss)
            exp.metric('test_loss', metrics['loss'])
            exp.metric('test_acc', metrics['acc'])
            Functions.PrintFunc.info(f"{engine.state.epoch} epoch End. Time Spent: {timer.value()}s")
            print(f"LR: {optim.param_groups[0]['lr']}")

        # 学習の開始
        trainer.run(train_loader, max_epochs=n_epochs)


def lr_range_test(model, train_loader, loss, device):
    # LR range test
    trt_optim = torch.optim.SGD(model.parameters(), lr=1e-8, momentum=0.99)
    trt_scheduler = torch.optim.lr_scheduler.StepLR(trt_optim, step_size=1, gamma=10)
    trainer = create_supervised_trainer(model, trt_optim, loss, device=device)
    evaluator = create_supervised_evaluator(model, metrics={'nll-loss': Loss(loss)}, device=device)
    timer = Timer(average=False)
    timer.attach(trainer, start=Events.EPOCH_STARTED, pause=Events.EPOCH_COMPLETED)
    losses = []
    lr_list = []

    @trainer.on(Events.STARTED)
    def set_metrics(engine: Engine):
        setattr(engine.state, 'prev_loss', 1e10)

    @trainer.on(Events.EPOCH_STARTED)
    def log_start(engine: Engine):
        Functions.PrintFunc.success(f"{engine.state.epoch} epoch start.")

    @trainer.on(Events.EPOCH_COMPLETED)
    def log_loss_decrease_lr(engine: Engine):
        Functions.PrintFunc.info(f"{engine.state.epoch} epoch End. Time Spent: {timer.value(): .3f}s")

        lr_ = trt_optim.param_groups[0]['lr']
        lr_list.append(lr_)
        losses.append(engine.state.output)
        trt_scheduler.step()

        # lossが登り始めたら打ち切り。
        if engine.state.prev_loss < engine.state.output:
            Functions.PrintFunc.success("The Loss exceeded the prev loss. break.")
            Functions.PrintFunc.success(f"The last LR is {lr_: .1e}.")
            engine.terminate()

        engine.state.prev_loss = engine.state.output

    # 学習の開始
    trainer.run(train_loader, max_epochs=10)
    import pickle
    pickle.dump((lr_list, losses), open('lr_range_test.pkl', 'wb'))

