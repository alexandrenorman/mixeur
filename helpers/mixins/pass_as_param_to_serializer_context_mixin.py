class PassAsParamToSerializerContextMixin:
    def get_serializer_context(self, *args, **kwargs):
        context = super(
            PassAsParamToSerializerContextMixin, self
        ).get_serializer_context(*args, **kwargs)
        as_param = self.request.query_params.get("as")
        if as_param:
            context["as"] = as_param
        return context
