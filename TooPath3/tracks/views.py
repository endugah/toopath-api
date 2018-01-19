from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from TooPath3.devices.permissions import IsOwnerOrReadOnly
from TooPath3.models import Device, Track
from TooPath3.tracks.serializers import TrackSerializer


class TrackList(APIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(Device, pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj

    def get(self, request, d_pk):
        device = self.get_object(d_pk)
        tracks = Track.objects.filter(device=device)
        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request, d_pk):
        device = self.get_object(d_pk)
        request.data['device'] = device.did
        serializer = TrackSerializer(data=request.data)
        if serializer.is_valid():
            track = serializer.save()
            track_json = TrackSerializer(track).data
            return Response(track_json, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TrackDetail(APIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_object(self, pk, model_class):
        obj = get_object_or_404(model_class, pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj

    def get(self, request, d_pk, t_pk):
        self.get_object(d_pk, Device)
        track = self.get_object(t_pk, Track)
        serializer = TrackSerializer(track)
        return Response(serializer.data, status=HTTP_200_OK)

    def patch(self, request, d_pk, t_pk):
        self.get_object(d_pk, Device)
        track = self.get_object(t_pk, Track)
        serializer = TrackSerializer(track, data=request.data, partial=True)
        if serializer.is_valid():
            track_partial_updated = serializer.save()
            return Response(TrackSerializer(track_partial_updated).data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, d_pk, t_pk):
        self.get_object(d_pk, Device)
        track = self.get_object(t_pk, Track)
        serializer = TrackSerializer(track, data=request.data)
        if serializer.is_valid():
            track_partial_updated = serializer.save()
            return Response(TrackSerializer(track_partial_updated).data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, d_pk, t_pk):
        self.get_object(pk=d_pk, model_class=Device)
        track = self.get_object(pk=t_pk, model_class=Track)
        track.delete()
        return Response(status=HTTP_204_NO_CONTENT)
