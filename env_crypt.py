from env_crypt import cli

def run():
    """Main entry point into the cli.

    This runs the functions related to the given arguments.
    """
    args = cli.parse_args()
    kwargs = {}
    kwargs.update(vars(args))
    kwargs.pop('func')
    args.func(**kwargs)
    return


if __name__ == "__main__":
    run()
