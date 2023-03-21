import sys

import shortuuid
import six
from django.db.models import CharField


class GG_ShortUUIDField(CharField):
    """A field which stores a Short UUID value in base57 format. This may also have
    the Boolean attribute 'auto' which will set the value on initial save to a
    new UUID value (calculated using shortuuid's default (uuid4)). Note that while all
    UUIDs are expected to be unique we enforce this with a DB constraint.
    """

    def __init__(self, auto=True, *args, **kwargs) -> None:
        self.auto = auto
        # We store UUIDs in base57 format, which is fixed at 22 characters.
        kwargs["max_length"] = 25
        if auto:
            # Do not let the user edit UUIDs if they are auto-assigned.
            kwargs["editable"] = False
            kwargs["blank"] = False
        super(GG_ShortUUIDField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add: bool):
        """
        This is used to ensure that we auto-set values if required.
        See CharField.pre_save
        """
        idx_prefix = getattr(model_instance, "IDX_PREFIX", "idx")
        if len(idx_prefix) != 3:
            raise ValueError("Idx Prefix should be of 3 characters")
        value = super(GG_ShortUUIDField, self).pre_save(
            model_instance=model_instance, add=add
        )
        if self.auto and not value:
            value = idx_prefix + "_" + six.text_type(shortuuid.uuid())
            setattr(model_instance, self.attname, value)
        return value

    def formfield(self, **kwargs):
        if self.auto:
            return None
        return super(GG_ShortUUIDField, self).formfield(**kwargs)


try:
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules([], [r"^gg_shortuuidfield\.fields\.GG_ShortUUIDField"])
except ImportError:
    pass
