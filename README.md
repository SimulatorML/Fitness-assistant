# Fitness Assistant - Фитнес-помощник

## Описание проекта

Fitness Assistant - это персонализированный AI-помощник, созданный для помощи пользователям в достижении их целей в области физической активности и питания. Используя современные технологии и интерактивный подход, приложение предоставляет индивидуальные планы тренировок, анализ питания по фотографиям и мотивационные инструменты.

## Целевая аудитория

- Люди, стремящиеся к здоровому образу жизни.
- Начинающие и продолжающие спортсмены.
- Люди, желающие оптимизировать и сбалансировать свой рацион питания.

## Основной функционал

### Тренировки

- **Персональные программы:** Индивидуально адаптированные планы тренировок с учётом целей, уровня подготовки и ограничений пользователя.
- **Подбор активностей с учетом профиля пользователя**
- **Библиотека упражнений:** Подробные описания, инструкции упражнений.
- **Отслеживание прогресса:** Ведение статистики, динамика тренировок/активностей, графики и отчёты о достижениях.
- **Адаптация нагрузки:** Автоматическая корректировка тренировочного плана в зависимости от обратной связи и результатов пользователя.

### Питание

- **Анализ фото еды:** Использование компьютерного зрения для распознавания продуктов, оценки калорийности и питательной ценности блюд.
- **Советы по рациону:** Персональные рекомендации по улучшению питания и составлению сбалансированного меню.
- **Замена продуктов:** Рекомендации по здоровым аналогам для замены менее полезных ингредиентов.

### Мотивация и социальное взаимодействие

- **Достижения и награды:** Система геймификации, позволяющая зарабатывать баллы, внутренние соревнования между пользователя и бонусы за регулярные тренировки и правильное питание.
- **Визуализация прогресса:** Интерактивные графики, статистика, сравнительный анализ результатов.

## Техническая реализация

### Клиентская часть

- **Telegram-бот:** Основной интерфейс для быстрой и удобной коммуникации с пользователем.

### Серверная часть

- **API:** Реализация на базе FastAPI для обеспечения высокой скорости, производительности и масштабируемости.
- **Хранение данных:** PostgreSQL для структурированных данных и Redis для кэширования, что ускоряет обработку запросов.
- **AI/ML модели:**
    - API LLM: Для ведения естественного диалога, генерации персонализированных рекомендаций и поддержки коммуникации.
    - RAG (Retrieval Augmented Generation): Для поиска релевантной информации и формирования расширенных ответов используя Langchain

### Интеграции

- **Базы данных:** Подключение к специализированным базам данных продуктов питания и упражнений для получения актуальной информации.

## Пользовательский путь

### Онбординг

- Проведение базового интервью для определения уровня подготовки и целей (пол, возраст, вес, рост, уровень активности, опыт).
- Настройка персональных предпочтений и уведомлений.

### Ежедневное использование

- Получение индивидуального плана тренировок/активностей и рекомендаций по питанию.
- Мотивационные советы рекомендации.
- Возможность отправки фото еды для анализа.
- Получение оперативной обратной связи и советов.

### Отслеживание результатов

- Еженедельные и месячные отчёты о прогрессе.
- Корректировка целей и адаптация плана тренировок.
- Получение наград и лидерборд.

## Безопасность

- **Аутентификация:** Надёжная аутентификация через Telegram и, при необходимости, через дополнительные методы (например, двухфакторная аутентификация).
- **Резервное копирование:** Регулярное создание резервных копий для предотвращения потери данных.

## Метрики успеха

- **Активность пользователей:** 60% пользователей остаются активными через месяц после регистрации.
- **Достижение целей:** 70% пользователей достигают поставленных целей.
- **Точность распознавания:** Распознавание еды по фото с точностью выше 85%.
- **Удовлетворенность пользователей:** Высокий уровень положительных отзывов и активное участие в сообществе.

## План развития

### Этап 1

- Запуск MVP через Telegram-бота с минимальным набором функций.
- Создание backend FastAPI приложения со взаимодействия с телеграм ботом
- Создания базы данных на Postgresql со взаимодействия с backend

### Этап 2

- Расширение аналитики, добавление новых режимов тренировок и углублённой персонализации.
- Внедрение командных соревнований, челленджей и дополнительных социальных функций.
- Интеграция с фитнес-трекерами и дополнительными источниками данных.

## Ограничения и предупреждения

- **Медицинская ответственность:** Приложение не заменяет консультацию врача. Все рекомендации носят информационный характер.
- **Форматы ввода:** Поддержка только текстовых сообщений и фотографий (на первом этапе).

## Дополнительные предложения по улучшению

- **Персонализация рекомендаций:** Использование алгоритмов машинного обучения для анализа истории активности и более точного подбора рекомендаций.
- **Интерактивное обучение:** Внедрение обучающих материалов (видео, статьи, советы) для повышения осведомлённости о правильном питании и тренировках.
- **Обратная связь:** Встроенная система сбора отзывов для постоянного улучшения функционала и качества рекомендаций.
- **Мобильное приложение:** В дальнейшем разработка нативных мобильных приложений для Android и iOS для расширения функциональности и удобства пользователей.
