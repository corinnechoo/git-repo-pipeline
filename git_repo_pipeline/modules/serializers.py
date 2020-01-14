from rest_framework import serializers


class PipelineInputSerializer(serializers.Serializer):
    """
        Checks that the json body has a valid format.

        Parameters
        ----------
        arg1 : dict
            Request body received from user

        Returns
        -------
        error
            the json body unchanged if valid, else an exception is raised

        """
    owner = serializers.CharField(required=True, max_length=128)
    repository = serializers.CharField(required=True, max_length=128)


class InputSerializer(serializers.Serializer):
    """
        Checks that the json body has a valid format. The datefield format is 
        set to default, which means it should be in the format 'yyyy-mm-dd'

        Parameters
        ----------
        arg1 : dict
            Request body received from user

        Returns
        -------
        error
            the json body unchanged if valid, else an exception is raised

        """
    owner = serializers.CharField(required=True, max_length=128)
    repository = serializers.CharField(required=True, max_length=128)
    start_date = serializers.DateField(required=True, input_formats=['%Y-%m-%d'])
    end_date = serializers.DateField(required=False, allow_null=True)

