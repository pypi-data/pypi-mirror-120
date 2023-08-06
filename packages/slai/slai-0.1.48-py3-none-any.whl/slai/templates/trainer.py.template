{{SLAI_TRAINER_IMPORTS}}


class Trainer:
    version = "{{SLAI_CURRENT_MODEL_VERSION}}"

    def __init__(self):
        pass

    def _train(self):
{{SLAI_TRAINER_CONTENTS}}

    def run(self, timeout={{SLAI_TRAINER_TIMEOUT}}):
        self._train()

if __name__ == "__main__":
    sys.modules["trainer"] = sys.modules[__name__]
    trainer = Trainer()
    trainer.run()
