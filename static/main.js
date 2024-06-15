async function updateStatus(token, newStatus, clientINN) {
    // Обновление текста кнопки
    document.getElementById('statusButton').innerText = newStatus;

    // Создание объекта с данными для отправки на сервер
    const data = {
        status_task: newStatus,
        token: token
    };

    // Отправка запроса на сервер
    try {
        const response = await fetch(`//users/clients/${clientINN}/status`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`);
        } else {
            const updatedClient = await response.json();
            console.log('Client status updated:', updatedClient);
        }
    } catch (error) {
        console.error('Error updating client status:', error);
    }
}