import posix_ipc
import sys

QUEUE_NAME = "/sys_prog_queue"

try:
    # Открываем существующую очередь без флага O_CREAT
    mq = posix_ipc.MessageQueue(QUEUE_NAME, flags=posix_ipc.O_CREAT)
except posix_ipc.ExistentialError:
    print("[ОШИБКА] Очередь не найдена в ядре. Сначала запустите ipc_sender.py!")
    sys.exit(1)

print("[ПРИЕМНИК] Успешно подключено к системной очереди. Начинаем чтение...")

# Запускаем бесконечный цикл чтения
while True:
    # receive() заблокирует поток, если сообщений в очереди нет
    binary_data, priority = mq.receive()

    message = binary_data.decode('utf-8')
    print(f"[ПРИЕМНИК] Получено из ядра: '{message}'")

    # Условие выхода для очистки очереди
    if "5" in message:
        print("[ПРИЕМНИК] Получено последнее сообщение.")
        break

# Закрываем и удаляем очередь
mq.close()
posix_ipc.unlink_message_queue(QUEUE_NAME)
print("[ПРИЕМНИК] Очередь удалена из операционной системы.")