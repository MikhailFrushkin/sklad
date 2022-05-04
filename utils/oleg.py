import speech_recognition


def mic(*args: tuple):
    """
    Запись и распознавание аудио
    """
    import speech_recognition as sr
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone(device_index=1)

    with microphone:
        recognized_data = ""

        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return

        # использование online-распознавания через Google
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет происходит выброс ошибки
        except speech_recognition.RequestError:
            print("Check your Internet Connection, please")

        return recognized_data


if __name__ == "__main__":
    print(mic())

# def mic():
#     sr = speech_recognition.Recognizer()
#     sr.pause_threshold = 0.5
#
#     with speech_recognition.Microphone() as mic:
#         sr.adjust_for_ambient_noise(source=mic, duration=1)
#         audio = sr.listen(source=mic)
#         query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
#     return query
