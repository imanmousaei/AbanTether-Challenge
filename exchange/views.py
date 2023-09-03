import json

from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from exchange.models import Video, EducationalBoxV1, VideoQuestion, EducationalBoxV2, EducationalV2Page
from exchange.serializers import EducationalBoxV1Serializer, EducationalQuestionSerializer, \
    EducationalBoxV2Serializer
from quizes.models import Audio, Choice, Image
from quizes.utils import extract_id


def body_parser(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    return body


class PlaceOrderView(APIView):
    def post(self, request):
        error = False
        success = True

        try:
            body = body_parser(request)
            serializer = EducationalQuestionSerializer(data=body)
            if serializer.is_valid():
                vqs = serializer.save()
                statuss = status.HTTP_201_CREATED

                for choice_dict in body['choices']:
                    try:
                        is_correct = float(choice_dict['is_correct'])
                    except:
                        is_correct = 0

                    number = choice_dict.get('number', None)
                    choice = Choice(text=choice_dict['choice'], is_correct=is_correct, number=number)
                    choice.save()

                    vqs.choices.add(choice)


                sound_id = extract_id(body.get('sound', ''))
                if sound_id is not None:
                    audio = Audio.objects.get(pk=sound_id)
                    vqs.sound = audio

                sound_if_correct_id = extract_id(body.get('sound_if_correct_id', ''))
                if sound_if_correct_id is not None:
                    audio = Audio.objects.get(pk=sound_if_correct_id)
                    vqs.sound_if_correct = audio

                sound_if_wrong_id = extract_id(body.get('sound_if_wrong_id', ''))
                if sound_if_wrong_id is not None:
                    audio = Audio.objects.get(pk=sound_if_wrong_id)
                    vqs.sound_if_wrong = audio

                vqs.save()
            else:
                error = serializer.errors.__str__()
                success = False
                statuss = status.HTTP_400_BAD_REQUEST

            response = {
                'success': success,
                'error': str(error),
                'question': serializer.data
            }
            return Response(response, statuss)

        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': str(e),
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)


    def patch(self, request):
        error = False
        success = True

        try:
            body = body_parser(request)
            question = VideoQuestion.objects.get(pk=body['pk'])
            serializer = EducationalQuestionSerializer(data=body, instance=question)
            if serializer.is_valid():
                vqs = serializer.save()
                statuss = status.HTTP_201_CREATED

                vqs.choices.all().delete()
                vqs.choices.clear()
                for choice_dict in body['choices']:
                    try:
                        is_correct = float(choice_dict['is_correct'])
                    except:
                        is_correct = 0

                    number = choice_dict.get('number', None)
                    choice = Choice(text=choice_dict['choice'], is_correct=is_correct, number=number)
                    choice.save()

                    vqs.choices.add(choice)


                sound_id = extract_id(body.get('sound', ''))
                if sound_id is not None:
                    audio = Audio.objects.get(pk=sound_id)
                    vqs.sound = audio

                sound_if_correct_id = extract_id(body.get('sound_if_correct_id', ''))
                if sound_if_correct_id is not None:
                    audio = Audio.objects.get(pk=sound_if_correct_id)
                    vqs.sound_if_correct = audio

                sound_if_wrong_id = extract_id(body.get('sound_if_wrong_id', ''))
                if sound_if_wrong_id is not None:
                    audio = Audio.objects.get(pk=sound_if_wrong_id)
                    vqs.sound_if_wrong = audio

                vqs.save()
            else:
                error = serializer.errors.__str__()
                success = False
                statuss = status.HTTP_400_BAD_REQUEST

            response = {
                'success': success,
                'error': str(error),
                'question': serializer.data
            }
            return Response(response, statuss)

        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': str(e),
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            pk = self.request.GET.get('id')

            educationals = None
            if pk:
                educationals = VideoQuestion.objects.filter(pk=pk)
            else:
                educationals = VideoQuestion.objects.all()

            response = {
                'success': True,
                'items': EducationalQuestionSerializer(educationals, many=True).data
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            response = {
                'success': False,
                'error': str(e),
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        msg = 'successfully deleted'
        success = True
        statuss = status.HTTP_200_OK

        try:
            quiz = VideoQuestion.objects.get(pk=pk)
            quiz.delete()
        except:
            success = False
            msg = f'سوالی با آیدی {pk} وجود ندارد'
            statuss = status.HTTP_400_BAD_REQUEST

        response = {
            'success': success,
            'error': msg,
        }
        return Response(response, statuss)


class EducationalV1View(APIView):
    def post(self, request):
        error = False
        success = True

        try:
            body = body_parser(request)
            serializer = EducationalBoxV1Serializer(data=body)
            if serializer.is_valid():
                box = serializer.save()
                statuss = status.HTTP_201_CREATED

                video_id = extract_id(body.get('video_id', ''))
                if video_id is not None:
                    video = Video.objects.get(pk=video_id)
                    box.video = video


                for qs_dict in body['questions']:
                    qspk = qs_dict.get('question_id', '')
                    try:
                        qs = VideoQuestion.objects.get(pk=qspk)
                    except:
                        response = {
                            'success': False,
                            'error': f'سوالی با آیدی {qspk} وجود ندارد',
                        }
                        return Response(response, status.HTTP_400_BAD_REQUEST)

                    box.questions.add(qs)
                box.save()
            else:
                error = serializer.errors.__str__()
                success = False
                statuss = status.HTTP_400_BAD_REQUEST

            response = {
                'success': success,
                'error': str(error),
                'question': serializer.data
            }
            return Response(response, statuss)

        except Exception as e:
            response = {
                'success': False,
                'error': str(e),
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        error = False
        success = True

        try:
            body = body_parser(request)
            boxv1 = EducationalBoxV1.objects.get(pk=body['pk'])
            serializer = EducationalBoxV1Serializer(data=body, instance=boxv1)
            if serializer.is_valid():
                box = serializer.save()
                statuss = status.HTTP_201_CREATED

                video_id = extract_id(body.get('video_id', ''))
                if video_id is not None:
                    video = Video.objects.get(pk=video_id)
                    box.video = video

                video_id = extract_id(body.get('video', ''))
                if video_id is not None:
                    video = Video.objects.get(pk=video_id)
                    box.video = video

                box.questions.all().delete()
                box.questions.clear()
                for qs_dict in body['questions']:
                    qspk = qs_dict.get('question_id', '')
                    try:
                        qs = VideoQuestion.objects.get(pk=qspk)
                    except:
                        response = {
                            'success': False,
                            'error': f'سوالی با آیدی {qspk} وجود ندارد',
                        }
                        return Response(response, status.HTTP_400_BAD_REQUEST)

                    box.questions.add(qs)
                box.save()
            else:
                error = serializer.errors.__str__()
                success = False
                statuss = status.HTTP_400_BAD_REQUEST

            response = {
                'success': success,
                'error': str(error),
                'question': serializer.data
            }
            return Response(response, statuss)

        except Exception as e:
            response = {
                'success': False,
                'error': str(e),
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            pk = self.request.GET.get('id')

            educationals = None
            if pk:
                educationals = EducationalBoxV1.objects.filter(pk=pk)
            else:
                educationals = EducationalBoxV1.objects.all()

            response = {
                'success': True,
                'items': EducationalBoxV1Serializer(educationals, many=True).data
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            response = {
                'success': False,
                'error': str(e),
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        msg = 'successfully deleted'
        success = True
        statuss = status.HTTP_200_OK

        try:
            educational = EducationalBoxV1.objects.get(pk=pk)
            educational.delete()
        except:
            success = False
            msg = f'باکسی با آیدی {pk} وجود ندارد'
            statuss = status.HTTP_400_BAD_REQUEST

        response = {
            'success': success,
            'error': msg,
        }
        return Response(response, statuss)


class EducationalV2View(APIView):
    def post(self, request):
        error = False
        success = True

        try:
            body = body_parser(request)
            serializer = EducationalBoxV2Serializer(data=body)
            if serializer.is_valid():
                box = serializer.save()
                statuss = status.HTTP_201_CREATED

                i = 0
                box.pages.all().delete()
                box.pages.clear()
                for choice_dict in body['choices']:
                    i += 1
                    page = EducationalV2Page(number=i)
                    page.save()

                    qspk = choice_dict.get('question_id', '')
                    try:
                        qs = VideoQuestion.objects.get(pk=qspk)
                        page.question = qs
                    except:
                        response = {
                            'success': False,
                            'error': f'سوالی با آیدی {qspk} وجود ندارد',
                        }
                        return Response(response, status.HTTP_400_BAD_REQUEST)

                    text = choice_dict.get('text', '')
                    if text:
                        page.text = text

                    audio_id = extract_id(choice_dict.get('sound', ''))
                    if audio_id is not None:
                        audio = Audio.objects.get(pk=audio_id)
                        page.sound = audio

                    image_id = extract_id(choice_dict.get('image', ''))
                    if image_id is not None:
                        image = Image.objects.get(pk=image_id)
                        page.image = image

                    page.save()
                    box.pages.add(page)

                box.save()
            else:
                error = serializer.errors.__str__()
                success = False
                statuss = status.HTTP_400_BAD_REQUEST

            response = {
                'success': success,
                'error': str(error),
                'question': serializer.data
            }
            return Response(response, statuss)

        except Exception as e:
            response = {
                'success': False,
                'error': str(e),
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        error = False
        success = True

        try:
            body = body_parser(request)
            boxv2 = EducationalBoxV2.objects.get(pk=body['pk'])
            serializer = EducationalBoxV2Serializer(data=body, instance=boxv2)
            if serializer.is_valid():
                box = serializer.save()
                statuss = status.HTTP_201_CREATED

                i = 0
                box.pages.all().delete()
                box.pages.clear()
                for choice_dict in body['pages']:
                    i += 1
                    page = EducationalV2Page(number=i)
                    page.save()

                    qspk = choice_dict.get('question_id', '')
                    try:
                        qs = VideoQuestion.objects.get(pk=qspk)
                        page.question = qs
                    except:
                        response = {
                            'success': False,
                            'error': f'سوالی با آیدی {qspk} وجود ندارد',
                        }
                        return Response(response, status.HTTP_400_BAD_REQUEST)

                    text = choice_dict.get('text', '')
                    if text:
                        page.text = text


                    audio_id = extract_id(choice_dict.get('sound', ''))
                    print(audio_id)
                    if audio_id is not None:
                        audio = Audio.objects.get(pk=audio_id)
                        page.sound = audio

                    print('here2')
                    image_id = extract_id(choice_dict.get('image', ''))
                    if image_id is not None:
                        image = Image.objects.get(pk=image_id)
                        page.image = image

                    print('here3')
                    page.save()
                    box.pages.add(page)

                box.save()
            else:
                error = serializer.errors.__str__()
                success = False
                statuss = status.HTTP_400_BAD_REQUEST

            response = {
                'success': success,
                'error': str(error),
                'question': serializer.data
            }
            return Response(response, statuss)

        except Exception as e:
            response = {
                'success': False,
                'error': str(e),
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            pk = self.request.GET.get('id')

            educationals = None
            if pk:
                educationals = EducationalBoxV2.objects.filter(pk=pk)
            else:
                educationals = EducationalBoxV2.objects.all()

            response = {
                'success': True,
                'items': EducationalBoxV2Serializer(educationals, many=True).data
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            response = {
                'success': False,
                'error': str(e),
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        msg = 'successfully deleted'
        success = True
        statuss = status.HTTP_200_OK

        try:
            educational = EducationalBoxV2.objects.get(pk=pk)
            educational.delete()
        except:
            success = False
            msg = f'باکسی با آیدی {pk} وجود ندارد'
            statuss = status.HTTP_400_BAD_REQUEST

        response = {
            'success': success,
            'error': msg,
        }
        return Response(response, statuss)


# file upload
class VideoUploadView(APIView):
    parser_classes = (MultiPartParser, )

    def post(self, request):
        try:
            file = request.FILES['files']
        except:
            file = request.FILES['file']

        video = Video(video=file)
        video.save()

        # image.image = settings.WEBSITE_BACKEND_URL + image.image
        # image.save()

        response = {
            'success': True,
            'id': video.id
        }
        return Response(response, status=status.HTTP_201_CREATED)

