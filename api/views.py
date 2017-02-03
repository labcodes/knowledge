from links.models import Link
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class CreateSlackNewLinkView(APIView):

    def post(self, request):
        text = request.POST.get('text')
        user_id = request.POST.get('user_id')

        try:
            Link.objects.create_from_slack(text, user_id)
        except (ValueError, ConnectionError):
            return Response({
                'text': 'Your Link is not valid. Please check your url.'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=201)
