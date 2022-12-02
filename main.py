import os,re


def post(querry):
    # пишет в cmd запрос
    global found
    command = querry
    pipe = os.popen(command)
    # записываем получившийся ответ в переменную
    output = str(pipe.read())
    # Очищаем от не нужного, пишем только то, что между маркерами ""
    m = re.search('"(.+?)"', output)
    if m:
        found = m.group(1)
    print(found)
    return found


def postK(querry):
    command = querry
    pipe = os.popen(command)
    output = str(pipe.read())
    return output

# Вставляем данные в рест ссылку
def addTandV_in_querry(text, vopros, link):
    # REST API Тимура
    # ответ на вопрос
    zapros = 'curl -X POST "" -H "accept: application/json" -H "Content-Type: application/json" -d "{\\"context_raw\\":[\\"\\"],\\"question_raw\\":[\\"\\"]}"'
    index = zapros.find('\\"],')
    output_line = zapros[:index] + text + zapros[index:]

    index = output_line.find('\\"]}"')
    final_str1 = output_line[:index] + vopros + output_line[index:]

    index = final_str1.find('" -H')
    final_str2 = final_str1[:index] + link + final_str1[index:]
    return final_str2

# Вставляем данные в рест ссылку
def VandV_in_querry(text1, text2, link):
    # REST API Кости
    # ответ сравнивает по смыслу
    zapros = 'curl -X POST "" -H "accept: application/json" -H "Content-Type: application/json" -d "{\\"text_a\\":[\\"\\"],\\"text_b\\":[\\"\\"]}"'
    index = zapros.find('\\"],')
    output_line = zapros[:index] + text1 + zapros[index:]

    index = output_line.find('\\"]}"')
    final_str1 = output_line[:index] + text2 + output_line[index:]

    index = final_str1.find('" -H')
    final_str2 = final_str1[:index] + link + final_str1[index:]
    return final_str2

def pomechaemDubli(l):
    k=0
    for i in l:
        k = k + 1
        for j in l:
            if postK(VandV_in_querry(i,j,linkKostya)) == "[1]" and l.index(i)!=l.index(j):
               idVoprosov[l.index(i)] = k
               idVoprosov[l.index(j)] = k
    deleteDubl(idVoprosov)

def deleteDubl(idVoprosov):
    n = []
    for i in idVoprosov:
        if i not in n:
            n.append(i)
        else:
            # listAnswers.pop(idVoprosov.index(i))
            listVoprosov.pop(idVoprosov.index(i))

def deleteAnswer(an):
    # делим строку на слова
    words = an.split(' ')
    # фрагмент, по которому будем удалять слова
    when = 'When'
    ans = '?'
    # новый список оставшихся слов
    an2 = []
    for word in words:
        if when not in word:
            an2.append(word)
    an = ' '.join(an2)
    an2 = []
    words = an.split(' ')
    for word in words:
        if ans not in word:
            an2.append(word)
    return ' '.join(an2)

# Нужно сделать из post и postK одну функцию
# VandV_in_querry и addTandV_in_querry тоже одна функция, в нее
# нужно еще передавать поля либо text_a, text_b либо context_raw question_raw  также, как
# как я делаю с текст1 и текст2 параметрами функции
# Ну и дописать удаление дублей с пометкой дублей + потом просто массив с конечными вопросами послать в post
if __name__ == '__main__':
    # Модель называется - Ответы только на не дублирующиеся вопросы

    listVoprosov = []
    listVoprosov1 = []
    listAnswers = []
    idVoprosov = []
    linkKostya = "https://5054-109-200-102-5.eu.ngrok.io/model" # пока с /model в конце
    linkTimur = "https://4531-2a01-540-a15-4800-2991-1cd4-708c-a7a.eu.ngrok.io/model"

    text = "Night falls, all the residents of the city went to sleep, and the criminals woke up."

    vopros1 = "When all the residents of the city went to sleep ?"
    vopros2 = "When residents went to sleep ?"
    vopros3 = "When night falls ?"
    listVoprosov.append(vopros1)
    listVoprosov.append(vopros2)
    listVoprosov.append(vopros3)

    print("Предложение: ", text)

    # заполняю айдишники вопросов нулями, по этому массиву будем помечать
    # 1 тех, которые одинаковые
    # удаляем вопросительные части для сравнения смыслов вопросов
    for i in range(len(listVoprosov)):
        print("Заданные вопросы: ", listVoprosov[i])
        idVoprosov.append(0)
        listVoprosov1.append(deleteAnswer(listVoprosov[i]))

    pomechaemDubli(listVoprosov1)

    # отвечаем на вопросы
    for i in range(len(listVoprosov)):
        a111 = post(addTandV_in_querry(text, listVoprosov[i], linkTimur))
        listAnswers.append(a111)
    # вывод ответов на вопросы

    for i in range(len(listVoprosov)):
        print("Вопрос: ", listVoprosov[i], " Ответ: ", listAnswers[i])