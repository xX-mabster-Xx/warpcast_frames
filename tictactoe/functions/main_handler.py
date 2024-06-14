import json
import requests
import base64


def check_winner(board_str):
    # Проверка длины строки
    if len(board_str) != 9:
        raise ValueError("Длина строки должна быть 9 символов.")
    
    # Преобразование строки в двумерный массив
    board = [list(board_str[i:i+3]) for i in range(0, 9, 3)]
    
    # Определение возможных линий для победы (строки, столбцы, диагонали)
    lines = []
    
    # Добавление строк
    lines.extend(board)
    
    # Добавление столбцов
    for col in range(3):
        lines.append([board[row][col] for row in range(3)])
    
    # Добавление диагоналей
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2-i] for i in range(3)])
    
    # Проверка каждой линии на победу
    for line in lines:
        if line[0] == line[1] == line[2] and line[0] != '0':
            return line[0]
    
    return '0'  # Возвращаем '0' если никто не победил

def return_main(event, context):

    if 'board' in event['params'] and len(event['params']['board']) == 9 and len(event['params']['board'].replace('0','').replace('1', '').replace('2', '')) == 0:
        winner = check_winner(event['params']['board'])
        og_markup = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta property="og:title" content="tictactoe">
                <meta property="fc:frame" content="vNext">
                <meta property="fc:frame:image:aspect_ratio" content="1:1">
                <meta property="fc:frame:image" content="https://d5dpp5ri7kobehnatge0.apigw.yandexcloud.net/tictactoe?board={event['params']['board']}&q={'win' if winner != '0' else 'draw'}">
                <meta property="fc:frame:button:1" content="Play!">
                <meta property="fc:frame:button:2" content="Creator">
                <meta property="fc:frame:button:2:action" content="link">
                <meta property="fc:frame:button:2:target" content="https://warpcast.com/xmabsterx">
                <meta property="og:image" content="https://d5dpp5ri7kobehnatge0.apigw.yandexcloud.net/tictactoe?board={event['params']['board']}&q={'win' if winner != '0' else 'draw'}">
            </head>
            <body>
                <h1>Frame Content</h1>
            </body>
        </html>
        """
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': og_markup,
        }

    og_markup = """
    <!DOCTYPE html>
    <html>
        <head>
            <meta property="og:title" content="tictactoe">
            <meta property="fc:frame" content="vNext">
            <meta property="fc:frame:image:aspect_ratio" content="1:1">
            <meta property="fc:frame:image" content="https://d5dpp5ri7kobehnatge0.apigw.yandexcloud.net/tictactoe?board=000000000">
            <meta property="fc:frame:input:text" content="Enter place(a1-c3)">
            <meta property="fc:frame:button:1" content="Confirm">
            <meta property="og:image" content="https://d5dpp5ri7kobehnatge0.apigw.yandexcloud.net/tictactoe?board=000000000">
        </head>
        <body>
            <h1>Frame Content</h1>
        </body>
    </html>
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': og_markup,
    }


def validateMessage(protobuf):
    url = "https://hub.pinata.cloud/v1/validateMessage"
    mbyts = bytes.fromhex(protobuf)
    headers = {
        "Content-Type": "application/octet-stream"
    }
    response = requests.post(url, headers=headers, data=mbyts)
    if response.status_code == 200 and response.json()['valid']:
        return response.json()['message']['data']


def on_post(event, context):
    # print(event, context)
    print(event)
    data = validateMessage(json.loads(event.get('body')).get('trustedData').get('messageBytes'))
    # text = str(data['fid'])
    place = base64.b64decode(str(data['frameActionBody']['inputText'])).decode('utf-8')
    place_str = base64.b64decode(str(data['frameActionBody']['state'])).decode('utf-8')
    if len(place_str) != 9:
        place_str = '000000000'
    
    pic_url = f"https://d5dpp5ri7kobehnatge0.apigw.yandexcloud.net/tictactoe?board={place_str}"

    if len(place) == 0:
        og_markup = """
        <!DOCTYPE html>
        <html>
            <head>
                <meta property="og:title" content="tictactoe">
                <meta property="fc:frame" content="vNext">
                <meta property="fc:frame:image:aspect_ratio" content="1:1">
                <meta property="fc:frame:image" content="https://d5dpp5ri7kobehnatge0.apigw.yandexcloud.net/tictactoe?board=000000000">
                <meta property="fc:frame:input:text" content="Enter place(a1-c3)">
                <meta property="fc:frame:button:1" content="Confirm">
                <meta property="og:image" content="https://d5dpp5ri7kobehnatge0.apigw.yandexcloud.net/tictactoe?board=000000000">
            </head>
            <body>
                <h1>Frame Content</h1>
            </body>
        </html>
        """
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': og_markup,
        }

    if len(place) != 2 or place[1] not in ['1','2','3'] or place[0] not in ['a','b','c']:
        og_markup = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta property="og:title" content="tictactoe">
                <meta property="fc:frame" content="vNext">
                <meta property="fc:frame:image:aspect_ratio" content="1:1">
                <meta property="fc:frame:image" content="{pic_url}">
                <meta property="fc:frame:input:text" content="Not correct(a1-c3)">
                <meta property="fc:frame:button:1" content="confirm">
                <meta property="fc:frame:state" content="{place_str}">
                <meta property="og:image" content="{pic_url}">
            </head>
            <body>
                <h1>Frame Content</h1>
            </body>
        </html>
        """
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': og_markup,
        }
    index = 3 * (ord(place[0]) - ord('a')) + int(place[1]) - 1
    if place_str[index] != '0':
        og_markup = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta property="og:title" content="tictactoe">
                <meta property="fc:frame" content="vNext">
                <meta property="fc:frame:image:aspect_ratio" content="1:1">
                <meta property="fc:frame:image" content="{pic_url}">
                <meta property="fc:frame:input:text" content="Here is {'cross' if place_str[index] == '1' else 'circle'} already">
                <meta property="fc:frame:button:1" content="confirm">
                <meta property="fc:frame:state" content="{place_str}">
                <meta property="og:image" content="{pic_url}">
            </head>
            <body>
                <h1>Frame Content</h1>
            </body>
        </html>
        """
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': og_markup,
        }
    place_str = place_str[:index] + ('1' if len(place_str.replace('0','')) % 2 == 0 else '2') + place_str[index + 1:]
    if check_winner(place_str) == '0' and len(place_str.replace('0','')) < 9:
        pic_url = f"https://d5dpp5ri7kobehnatge0.apigw.yandexcloud.net/tictactoe?board={place_str}"
        og_markup = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta property="og:title" content="tictactoe">
                <meta property="fc:frame" content="vNext">
                <meta property="fc:frame:image:aspect_ratio" content="1:1">
                <meta property="fc:frame:image" content="{pic_url}">
                <meta property="fc:frame:input:text" content="place">
                <meta property="fc:frame:button:1" content="confirm">
                <meta property="fc:frame:state" content="{place_str}">
                <meta property="og:image" content="{pic_url}">
            </head>
            <body>
                <h1>Frame Content</h1>
            </body>
        </html>
        """
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': og_markup,
        }
    elif check_winner(place_str) != '0':
        pic_url = f"https://d5dpp5ri7kobehnatge0.apigw.yandexcloud.net/tictactoe?board={place_str}&q=victory"
        og_markup = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta property="og:title" content="tictactoe">
                <meta property="fc:frame" content="vNext">
                <meta property="fc:frame:image:aspect_ratio" content="1:1">
                <meta property="fc:frame:image" content="{pic_url}">
                <meta property="fc:frame:button:1" content="Share">
                <meta property="fc:frame:button:1:action" content="link">
                <meta property="fc:frame:button:1:target" content="https://warpcast.com/~/compose?text=Wow!&embeds%5B%5D=https://d5dpp5ri7kobehnatge0.apigw.yandexcloud.net/warpcast?board={place_str}">
                <meta property="fc:frame:button:2" content="Creator">
                <meta property="fc:frame:button:2:action" content="link">
                <meta property="fc:frame:button:2:target" content="https://warpcast.com/xmabsterx">
                <meta property="fc:frame:state" content="{place_str}">
                <meta property="og:image" content="{pic_url}">
            </head>
            <body>
                <h1>Frame Content</h1>
            </body>
        </html>
        """
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': og_markup,
        }
    else:
        
        pic_url = f"https://d5dpp5ri7kobehnatge0.apigw.yandexcloud.net/tictactoe?board={place_str}&q=draw2"
        og_markup = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta property="og:title" content="tictactoe">
                <meta property="fc:frame" content="vNext">
                <meta property="fc:frame:image:aspect_ratio" content="1:1">
                <meta property="fc:frame:image" content="{pic_url}">
                <meta property="fc:frame:button:1" content="Share">
                <meta property="fc:frame:button:1:action" content="link">
                <meta property="fc:frame:button:1:target" content="https://warpcast.com/~/compose?text=Wow!&embeds%5B%5D=https://d5dpp5ri7kobehnatge0.apigw.yandexcloud.net/warpcast?board={place_str}">
                <meta property="fc:frame:button:2" content="Creator">
                <meta property="fc:frame:button:2:action" content="link">
                <meta property="fc:frame:button:2:target" content="https://warpcast.com/xmabsterx">
                <meta property="fc:frame:state" content="{place_str}">
                <meta property="og:image" content="{pic_url}">
            </head>
            <body>
                <h1>Frame Content</h1>
            </body>
        </html>
        """
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': og_markup,
        }


def handler(event, context):
    print(event, context)
    if event['httpMethod'] == 'GET': 
        return return_main(event, context)
    else:
        return on_post(event, context)


