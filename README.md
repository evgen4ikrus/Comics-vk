# Comics-vk
Утилита для автоматической публикации комиксов на стену группы [ВКонтакте](https://vk.com/).
### Установка
Для работы скрипта вам понадобится Python третьей версии.

Скачайте код с GitHub. Затем установите зависимости:

```sh
pip install -r requirements.txt
```
### Переменные окружения
1. Создайте файл .env в папке с проектом.

3. Получите client_id:

Создайте [фан-группу](https://vk.com/groups?tab=admin) и [приложение](https://dev.vk.com/) во ВКонтакте. В качестве типа приложения следует указать standalone.
Hажмите на кнопку “Редактировать” для нового приложения, в адресной строке вы увидите его client_id. Запишите его в .env.

3. Получите access_token:

Для получения access_token следуйте инструкции по [этой ссылке](https://dev.vk.com/api/access-token/implicit-flow-user) или проделайте простые шаги описанные ниже:

* Скопируйте и вставьте в адресную строку следующую строку:
```
https://oauth.vk.com/authorize?client_id={client_id}&response_type=token&scope=photos,groups,wall,offline
```
* Замените "{client_id}" на client_id полученный ранее. Если все сделано правильно, то вы увидите страницу, как на скриншоте:

![test](https://user-images.githubusercontent.com/67272160/180602969-be789ab9-6d69-481a-bb42-6922ca981631.png)

* Из адресной строки скопируйте свой access_token. Добавьте его в файл .env.

4. Получите group_id:

Пройдите по [ссылке](https://regvk.com/id/). В поле ввода вставьте ссылку на вашу группу [ВКонтакте](https://vk.com/). Добавьте group_id в файл .env.

Пример содержимого файла .env:
```
VK_CLIENT_ID=8124143
VK_ACCESS_TOKEN=vk1.a.4otQFIryvqi9P_Yt3kQ2_r7blKZ3F5ErkYcLxCMHBCKWwK_4tt36Fy_k8McC0dSu472mvbQqZ9aSNU-xtTg7KorN1OLikBlAkecXbTiGJDzC71eY0CUNnSwpWVRASa5cnRRE79nn3ETqXyWVJQk774AKxJ4TRy6GNxQGDg2nNAWb7J7awV_a5BCzbZAuy2v8
VK_GROUP_ID=204547928
```
### Использование
Запустите скрипт vk_comic.py:
```
python vk_comic.py
```
С сайта [xkcd.com](https://xkcd.com/) скачается случайный комикс про python и опубликуется на стене вашей группы ВКонтакте.

![image](https://user-images.githubusercontent.com/67272160/180603608-32815a0e-3c35-44ec-a16a-6e800337785d.png)
