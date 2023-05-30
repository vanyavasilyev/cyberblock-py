# CyberBlock: анализ блокчейн графовой базой данных и не только

В данном репозитории представлены инструменты для анализа блокчейн с помощью графовой базы данных и анализа транзакций конкретных аккаунтов. 

Основной задачей был анализ миксеров и подобных сущностей. Анализ таковых на основе zero-knowledge протоколов представлен [тут](./docs/zero-knowledge-proofs.md).

## Анализ с помощью графа

В [`src`](./src) представлено приложение, позволяющее объеденить в себе алгоритмы сканирования блокчейн, взаимодействия с БД, анализа графа с помощью БД. Архитектура представлена в [файле](./docs/architecture.md). Блокчейн хранится в виде графа, вершины которого - адреса, а рёбра - транзакции (как normal, так и internal).

Реализованы методы загрузки ethereum и подобных сетей в neo4j. Доступны 2 алгоритма сканирования: BFS и построение входящих/выходящих деревьев. Реализован функционал исполнения ряда запросов к БД, отражающих свойства сущностей блокчейн. Помимо базовых запросов для перечисления рёбер и т.д. доступны такие запросы:

- in_out_ratio - вычисление для всех адресов соотношения числа нод, с которых были направлены транзакции на адрес, к числу тех, на которые шли транзакции с адреса. Может быть полезно для поиска аккаунтов, распределяющих средства многих пользователей между ограниченной группой нод, тем самым "перемешивая" их.

- make_total_edges - строит в графе ребра, объединяющие множество транзакций между парой адресов с вычислением общей суммы.

- set_flows_to/set_floows_from - вычисляет потенциальные объёмы движения эфира на/от адреса в графе, загруженным сканером направленных деревьев. Подробнее в [файле](./docs/flow.md).

Добавления нового функционала анализа с помщью запросов к neo4j происходит через дополнение [файла](./data/neo4j_queries.json) запросом. 

## Отдельные скрипты

В [директории](./scripts/) представлены 2 скрипта для деанонимизации движения средств через tornado, railgun и подобные проекты.

 `railgun_balances.py` позволяет группировать адреса на основе схожего объёма переведенных/полученных среств для контрактов, логика которых схожа с Railgun. Получатели в группах, вероятнее всего, получили средства именно от какого-то из неаккуратных отправителей в группе.

 `tornado_deanon.py` объединяет цепочки вызовов `deposit` и `withdraw` на tornado-миксерах в заданных временных рамках и в таком порядке. С большой долей уверенности можно говорить, что такие события происходят в результате неосторожного использования контракта одним пользователем.  