from links.models import Link
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class CreateSlackNewLinkView(APIView):

    def post(self, request):
        text = request.POST.get('text')

        try:
            Link.objects.create_from_slack(text)
        except ValueError:
            return Response({
                'text': 'Your Link is not valid.\nPlease check the syntax: title: url'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=201)
