# emotion_detection.py

import requests
import json

def emotion_detector(text_to_analyze):
    """
    Ejecuta la detección de emociones utilizando la API de Watson NLP
    y formatea la salida según los requisitos.

    Args:
        text_to_analyze (str): El texto que se analizará para detectar emociones.

    Returns:
        dict or None: Un diccionario con las puntuaciones de ira, desagrado, miedo, alegría,
                      tristeza y la emoción dominante, o None si ocurre un error.
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    # Asegúrate de que el formato del JSON de entrada sea correcto
    input_json = { "raw_document": { "text": text_to_analyze } }

    try:
        # Añadido un timeout explícito de 10 segundos para evitar que se cuelgue indefinidamente
        response = requests.post(url, headers=headers, json=input_json, timeout=10)
        response.raise_for_status()  # Lanza una excepción para errores HTTP (4xx o 5xx)
        
        # Convierte el texto de respuesta en un diccionario utilizando las funciones de la biblioteca json.
        # Esto ya lo hacemos con response.json()
        response_data = response.json()
        
        # Extrae el conjunto requerido de emociones y sus puntajes.
        # La estructura es: response_data['document']['emotion']['predictions'][0]['emotion']
        emotions_scores = response_data['document']['emotion']['predictions'][0]['emotion']
        
        # Extraer las puntuaciones individuales
        anger_score = emotions_scores.get('anger', 0.0)
        disgust_score = emotions_scores.get('disgust', 0.0)
        fear_score = emotions_scores.get('fear', 0.0)
        joy_score = emotions_scores.get('joy', 0.0)
        sadness_score = emotions_scores.get('sadness', 0.0)

        # Escribe la lógica del código para encontrar la emoción dominante,
        # que es la emoción con el puntaje más alto.
        # Crear un diccionario para encontrar la dominante fácilmente
        all_emotions = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }
        
        # Encuentra la emoción con el puntaje más alto
        # Usamos .items() para obtener pares (nombre_emocion, puntaje)
        # key=lambda item: item[1] le dice a max() que compare por el segundo elemento del par (el puntaje)
        dominant_emotion_name = max(all_emotions.items(), key=lambda item: item[1])[0]
        
        # Modifica la función emotion_detector para que devuelva el siguiente formato de salida.
        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion_name
        }

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err} - Status: {response.status_code} - Response: {response.text}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error de conexión: {conn_err}. Asegúrate de tener conexión a Internet y que la URL de la API sea accesible.")
        return None
    except requests.exceptions.Timeout as timeout_err:
        print(f"Tiempo de espera agotado: {timeout_err}. La API tardó demasiado en responder.")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Error general en la solicitud: {req_err}")
        return None
    except json.JSONDecodeError as json_err:
        print(f"Error al decodificar JSON de la respuesta: {json_err} - Respuesta recibida: {response.text}")
        return None
    except KeyError as key_err:
        print(f"Clave no encontrada en la respuesta JSON: {key_err}. La estructura de respuesta de la API puede haber cambiado o ser inesperada.")
        print(f"Respuesta completa recibida: {response_data}")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None

# --- Bloque para pruebas locales (no se ejecuta al importar como módulo) ---
if __name__ == "__main__":
    print("--- Prueba local de la función emotion_detector ---")
    
    # Texto de prueba para verificar "joy"
    test_text_joy = "Estoy tan feliz de estar haciendo esto."
    result_joy = emotion_detector(test_text_joy)
    if result_joy:
        print(f"\nTexto analizado: '{test_text_joy}'")
        print(f"Resultado formateado: {result_joy}")
        print(f"Emoción dominante esperada: alegría. Emoción dominante obtenida: {result_joy['dominant_emotion']}")
    else:
        print(f"\nNo se pudieron detectar las emociones para: '{test_text_joy}'")

    # Otro texto de prueba, por ejemplo, para "sadness"
    test_text_sad = "Me siento un poco triste por las noticias."
    result_sad = emotion_detector(test_text_sad)
    if result_sad:
        print(f"\nTexto analizado: '{test_text_sad}'")
        print(f"Resultado formateado: {result_sad}")
        print(f"Emoción dominante esperada: tristeza. Emoción dominante obtenida: {result_sad['dominant_emotion']}")
    else:
        print(f"\nNo se pudieron detectar las emociones para: '{test_text_sad}'")

    # Otro texto de prueba, por ejemplo, para "anger"
    test_text_anger = "Estoy furioso con esta situación."
    result_anger = emotion_detector(test_text_anger)
    if result_anger:
        print(f"\nTexto analizado: '{test_text_anger}'")
        print(f"Resultado formateado: {result_anger}")
        print(f"Emoción dominante esperada: ira. Emoción dominante obtenida: {result_anger['dominant_emotion']}")
    else:
        print(f"\nNo se pudieron detectar las emociones para: '{test_text_anger}'")
