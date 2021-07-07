import io
import pandas
import csv
import uuid
from contextlib import closing
from django.db import connection

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from icecream.models import IceCream
from icecream.api.serializers import IceCreamSerializer


class IceCreamViewset(viewsets.ModelViewSet):
    permission_classes = []
    queryset = IceCream.objects.all()
    serializer_class = IceCreamSerializer

    @action(methods=["POST"], detail=False)
    def bulk_create(self, request, *args, **kwargs):

        uploaded_file = request.FILES["file"]
        file_stream = io.StringIO(uploaded_file.read().decode('utf-8'))
        csv_data = pandas.read_csv(file_stream, delimiter=',').to_dict('records')

        serializer = self.get_serializer(data=csv_data, many=True)
        serializer.is_valid(raise_exception=True)
        icecreams = serializer.save()
        return Response(data=IceCreamSerializer(icecreams, many=True).data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False)
    def bulk_upload(self, request, *args, **kwargs):
        uploaded_file = request.FILES["file"]
        file_stream = io.StringIO(uploaded_file.read().decode('utf-8'))
        csv_data = pandas.read_csv(file_stream, delimiter=',').to_dict('records')

        stream = io.StringIO()
        writer = csv.writer(stream, delimiter='\t')

        for row in csv_data:
            writer.writerow([str(uuid.uuid4()), row["name"]])
        stream.seek(0)

        with closing(connection.cursor()) as cursor:
            cursor.copy_from(
                file=stream,
                table=IceCream.objects.model._meta.db_table,
                sep='\t',
                columns=('id', 'name'),
            )
        return Response(data=csv_data, status=status.HTTP_200_OK)
