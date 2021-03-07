from .unpack_ids_mixin import UnpackIdsMixin


class UnpackTagsMixin(UnpackIdsMixin):
    """
    Mixin to apply on a ModelViewSet which transform registered fields from string containing ids to list of objects
    "1,2,3" => [<Obj id=1>, <Obj id=2>, <Obj id=3>]
    If a string passed, it will create a new instance of given model with given model name field
    "1,2,truc" =>  [<Obj id=1 name=...>, <Obj id=2 name=...>, <new Obj id=3 name="truc">]

    Should define unpackable fields like this :
    unpackable_fields = {'data_field_name': (ModelName, 'model_field_name')}
    """

    def get_item_id(self, word, options):
        """
        If given tag contain only digits, use it as id, else create the instance
        """

        item_id = None

        if word.isdigit():
            item_id = int(word)
        elif options:
            tag_model, tag_model_field = options
            existing_tag = tag_model.objects.filter(**{tag_model_field: word}).first()
            if existing_tag:
                item_id = existing_tag.id
            elif word != "":
                item_id = tag_model.objects.create(**{tag_model_field: word}).id
            else:
                return {"id": None}

        if item_id is not None:
            return {"id": item_id}
