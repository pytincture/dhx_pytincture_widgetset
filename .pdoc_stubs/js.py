class _JsStub:
    def __getattr__(self, name):
        return self

    def __call__(self, *args, **kwargs):
        return self

js = _JsStub()
