class MissingEnvVar(Exception):
    """
    Exception to raise when necessary environment variables are missing.
    """

    def __init__(self, missing):
        self.message = f"Missing environment variable(s): {', '.join(missing)}"
        super().__init__(self.message)
