import speech_recognition as sr

print("Available Microphones:")
print(sr.Microphone.list_microphone_names())
