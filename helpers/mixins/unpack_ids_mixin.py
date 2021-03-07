from django.db import transaction


class UnpackIdsMixin:
    """
    Mixin to apply on a ModelViewSet which transform registered fields from string containing ids to list of objects
    "1,2,3" => [<Obj id=1>, <Obj id=2>, <Obj id=3>]
    or
    "1,2,3" => [1, 2, 3]

    Should define unpackable fields like this :
    unpack to [{'id': 1}, {'id': 2}, {'id': 3}]
        unpackable_fields = ('data_field_name',)

    unpack to [1, 2, 3] :
        unpackable_fields = {'data_field_name': {'flat': True}}
    """

    unpackable_fields = ()

    def get_item_id(self, word, options):
        """
        If given tag contain only digits, use it as id
        """
        if word.isdigit():
            item_id = int(word)
            if isinstance(options, dict) and options.get("flat"):
                return item_id
            return {"id": item_id}
        return None

    def __unpack_field__(self, data, field_name):
        """
        Split value and replace field value by list of instances
        """
        value = data.get(field_name, None)
        if not isinstance(value, str):
            return  # If not string do not do anything
        options = None
        if isinstance(self.unpackable_fields, dict):
            options = self.unpackable_fields.get(field_name)
        word_list = value.split(",")
        items = []
        for word in word_list:
            item_id = self.get_item_id(word, options)
            if item_id:
                items.append(item_id)
        data[field_name] = items

    def __unpack_fields__(self, data):
        for field_name in self.unpackable_fields:
            self.__unpack_field__(data, field_name)

    def create(self, request, *args, **kwargs):
        with transaction.atomic():  # If object create fail rollback any tags creation
            self.__unpack_fields__(request.data)
            return super(UnpackIdsMixin, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        with transaction.atomic():  # If object create fail rollback any tags creation
            self.__unpack_fields__(request.data)
            return super(UnpackIdsMixin, self).update(request, *args, **kwargs)
