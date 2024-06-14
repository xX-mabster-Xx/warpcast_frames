from PIL import Image
import base64
from io import BytesIO


def handler(event, context):
    print(event)
    # empty = Image.open("/function/storage/data/blank.png")
    cross = Image.open("/function/storage/data/cross.png")
    nought = Image.open("/function/storage/data/circle.png")
    if 'board' not in event['params']:
        return {
            'statusCode': 400,
            'body': 'No params'
        }
    board_str = event['params']['board']
    if len(board_str) != 9:
        return {
            'statusCode': 400,
            'body': 'Invalid params'
        }
    if len(board_str.replace('0','').replace('1', '').replace('2', '')) != 0:
        return {
            'statusCode': 400,
            'body': 'Invalid params'
        }

    game_board = [list(board_str[i:i+3]) for i in range(0, 9, 3)]
    cell_size = cross.size
    # Создание нового изображения для доски
    board_size = (cell_size[0] * 3, cell_size[1] * 3)
    board_image = Image.open("/function/storage/data/tic_tac_toe_board.png")

    # Заполнение доски
    for row in range(3):
        for col in range(3):
            if game_board[row][col] == '1':
                board_image.paste(cross, (col * (cell_size[0]+2), row * (cell_size[1]+2)))
            elif game_board[row][col] == '2':
                board_image.paste(nought, (col * (cell_size[0]+2), row * (cell_size[1]+2)))

    if 'q' not in event['params']:
        img_byte_arr = BytesIO()
        board_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        # Кодирование изображения в base64
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'image/png',
                'Content-Transfer-Encoding': 'base64'
            },
            'body': img_base64,
            'isBase64Encoded': True
        }
    elif event['params']['q'] == 'win':
        won = Image.open("/function/storage/data/won.png")
        won.paste(board_image, (149, 240))
        img_byte_arr = BytesIO()
        won.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        # Кодирование изображения в base64
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'image/png',
                'Content-Transfer-Encoding': 'base64'
            },
            'body': img_base64,
            'isBase64Encoded': True
        }
    elif event['params']['q'] == 'draw':
        lose = Image.open("/function/storage/data/lose.png")
        lose.paste(board_image, (149, 240))
        img_byte_arr = BytesIO()
        lose.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        # Кодирование изображения в base64
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'image/png',
                'Content-Transfer-Encoding': 'base64'
            },
            'body': img_base64,
            'isBase64Encoded': True
        }
    elif event['params']['q'] == 'victory':
        lose = Image.open("/function/storage/data/victory.png")
        lose.paste(board_image, (149, 240))
        img_byte_arr = BytesIO()
        lose.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        # Кодирование изображения в base64
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'image/png',
                'Content-Transfer-Encoding': 'base64'
            },
            'body': img_base64,
            'isBase64Encoded': True
        }
    elif event['params']['q'] == 'draw2':
        lose = Image.open("/function/storage/data/draw.png")
        lose.paste(board_image, (149, 240))
        img_byte_arr = BytesIO()
        lose.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        # Кодирование изображения в base64
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'image/png',
                'Content-Transfer-Encoding': 'base64'
            },
            'body': img_base64,
            'isBase64Encoded': True
        }


    

    
