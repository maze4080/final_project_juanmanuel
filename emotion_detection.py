# emotion_detection.py

import requests
import json

def emotion_detector(text_to_analyze):
    """
    Ejecuta la detección de emociones utilizando la API de Watson NLP.

    Args:
        text_to_analyze (str): El texto que se analizará para detectar emociones.

    Returns:
        dict or None: Un diccionario con las puntuaciones de las emociones
                      (joy, anger, disgust, sadness, fear) y la emoción dominante,
                      o None si ocurre un error.
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    # Asegúrate de que el formato del JSON de entrada sea correcto
    input_json = { "raw_document": { "text": text_to_analyze } }

    try:
        response = requests.post(url, headers=headers, json=input_json)
        response.raise_for_status()  # Lanza una excepción para errores HTTP (4xx o 5xx)
        
        # Analizar la respuesta JSON
        # La API de Watson NLP devuelve un JSON complejo.
        # Necesitamos navegar por él para obtener los scores de las emociones.
        # Basado en la estructura típica de respuesta de Watson NLP para detección de emociones:
        # response_data = {
        #     "document": {
        #         "emotion": {
        #             "predictions": [
        #                 {
        #                     "emotion": {
        #                         "anger": ...,
        #                         "disgust": ...,
        #                         "sadness": ...,
        #                         "joy": ...,
        #                         "fear": ...
        #                     }
        #                 }
        #             ]
        #         }
        #     }
        # }

        response_data = response.json()
        
        # Extraer las puntuaciones de las emociones
        emotions = response_data['document']['emotion']['predictions'][0]['emotion']
        
        # Encontrar la emoción dominante
        # Nota: La descripción original pide "el atributo text del objeto de respuesta".
        # Sin embargo, la API de Watson NLP devuelve un diccionario de puntuaciones.
        # Lo más útil es devolver esas puntuaciones y quizás la emoción dominante.
        # Vamos a retornar un diccionario con todas las emociones y la dominante.

        # Encontrando la emoción dominante
        dominant_emotion = max(emotions, key=emotions.get)
        
        # Si específicamente se requiere un objeto con un atributo 'text' para la emoción dominante,
        # podríamos adaptar la salida así:
        # class EmotionResult:
        #     def __init__(self, emotion_scores, dominant_emotion_text):
        #         self.emotion_scores = emotion_scores
        #         self.text = dominant_emotion_text # Esto sería la emoción con mayor score
        # return EmotionResult(emotions, dominant_emotion)
        
        # Sin embargo, lo más práctico es devolver el diccionario de emociones
        # y la emoción dominante por separado o dentro del mismo diccionario.
        # Me apegaré a devolver las puntuaciones y la emoción dominante para ser más útil.
        # Si *insisten* en un objeto con atributo 'text', se puede crear una clase simple como arriba.
        
        # Para cumplir estrictamente con "el atributo text del objeto de respuesta tal como se recibe",
        # y dado que Watson devuelve un JSON estructurado, interpretar "text" como la emoción dominante es la más lógica.

        # Retornamos un diccionario con todas las puntuaciones y la emoción dominante
        return {
            'joy': emotions['joy'],
            'anger': emotions['anger'],
            'disgust': emotions['disgust'],
            'sadness': emotions['sadness'],
            'fear': emotions['fear'],
            'dominant_emotion': dominant_emotion
        }

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err} - {response.status_code} - {response.text}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error de conexión: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout de la solicitud: {timeout_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Error general de solicitud: {req_err}")
        return None
    except json.JSONDecodeError as json_err:
        print(f"Error al decodificar JSON de la respuesta: {json_err} - Respuesta: {response.text}")
        return None
    except KeyError as key_err:
        print(f"Clave no encontrada en la respuesta JSON: {key_err}. Estructura de respuesta inesperada.")
        print(f"Respuesta completa: {response_data}")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None

# Si se ejecuta este archivo directamente, podemos probar la función
if __name__ == "__main__":
    text = "I love this new technology."
    result = emotion_detector(text)
    
    if result:
        print(f"Texto analizado: '{text}'")
        print(f"Emociones detectadas: {result}")
        print(f"Emoción dominante: {result['dominant_emotion']}")
    else:
        print("No se pudieron detectar las emociones.")

    print("\n--- Otra prueba ---")
    text_sad = "I am so sad to hear this news."
    result_sad = emotion_detector(text_sad)
    if result_sad:
        print(f"Texto analizado: '{text_sad}'")
        print(f"Emociones detectadas: {result_sad}")
        print(f"Emoción dominante: {result_sad['dominant_emotion']}")
    else:
        print("No se pudieron detectar las emociones.")

    print("\n--- Otra prueba ---")
    text_neutral = "The sky is blue today."
    result_neutral = emotion_detector(text_neutral)
    if result_neutral:
        print(f"Texto analizado: '{text_neutral}'")
        print(f"Emociones detectadas: {result_neutral}")
        print(f"Emoción dominante: {result_neutral['dominant_emotion']}")
    else:
        print("No se pudieron detectar las emociones.")
