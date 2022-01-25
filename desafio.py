import time
import aiohttp
import asyncio
from flask import jsonify
from flask_api import FlaskAPI

app = FlaskAPI(__name__)

start_time = time.time()
l = []

'''
    1 - source cross_env/bin/activate --> Ativar o ambiente preparado
    2 - python3 -m pip install -r requirements.txt --> Instalar os requisitos
    3 - Para rodar o programa: python3 desafio.py
    4 - Para obter a ordenação: curl -X GET http://127.0.0.1:5000/list_sorted 
'''

# def join_dict_values(dict):
#     final_list = []
#     for l in dict:
#         final_list += dict[l]
    # if final_list == sorted(final_list):
    #     print('Sucesso, as listas ordenadas pelos 2 métodos são iguais!', l)
    # else:
    #     print('Casa caiu, deu ruim!')
    # return final_list

# def paiva_sort(lista_desordenada):
#     print ('--Inciando ordenação--')
#     dict = {}
#     for i in range(0,11):
#         dict.update({i/10:[]})
#     for num in lista_desordenada:
#         for key in dict:
#             if num >= key and num < key + 0.1:
#                 if dict[key]:
#                     check = True
#                     for v in dict[key]:
#                         if num < v:
#                             dict[key].insert(dict[key].index(v), num)
#                             check = False
#                             break
#                     if check:
#                         dict[key].append(num)
#                 else:
#                     dict[key].append(num)
#     return join_dict_values(dict)

def paiva_part_v2(nums, low, high):
    pivot = nums[(low + high) // 2]
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while nums[i] < pivot:
            i += 1

        j -= 1
        while nums[j] > pivot:
            j -= 1

        if i >= j:
            return j

        nums[i], nums[j] = nums[j], nums[i]


def paiva_sort_v2(nums):
    print ('--Inciando ordenação--')
    def _paiva_sort(item, low, high):
        if low < high:
            split_i = paiva_part_v2(item, low, high)
            _paiva_sort(item, low, split_i)
            _paiva_sort(item, split_i + 1, high)

    _paiva_sort(nums, 0, len(nums) - 1)

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        #Infelizmente nao tive tempo para arrumar um jeito de parar o for quando a api retorna vazia. Fui pelo entendimento do tamanho da paginação.
        for page in range(1,15000):
            task = asyncio.ensure_future(get_list_data(session, page))
            tasks.append(task)
        await asyncio.gather(*tasks)
        

async def get_list_data(session, key):
    url = f'http://challenge.dienekes.com.br/api/numbers?page={key}'
    async with session.get(url) as response:
        response_data = await response.json()
        try:
            if not response_data['numbers']:
                # print('Fim', response_data['numbers'])
                return response_data
        except Exception as ex:
            # print('ValueError', ex)
            return

        l.extend(response_data['numbers'])
        # print(f'Teste data:{response_data}')
    


# l_sorted = paiva_sort(l)
# paiva_sort_v2(l)

# if l == sorted(l):
#     print('Sucesso, as listas ordenadas pelos 2 métodos são iguais!', l)
# else:
#     print('Falhou!')

# print("--- %s seconds ---" % (time.time() - start_time))


@app.route('/list_sorted', methods=['GET'])
def getSorted():
    asyncio.run(main())
    paiva_sort_v2(l)
    print("--- %s seconds ---" % (time.time() - start_time))
    return jsonify(l)


if __name__ == "__main__":
    app.run(debug=True)