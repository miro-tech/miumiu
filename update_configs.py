import json
import urllib.request

# Ссылки на ваши источники с конфигурациями
URLS = [
    "https://raw.githubusercontent.com/Mdrzxsony/nekome/refs/heads/main/configs",
    "https://raw.githubusercontent.com/Mdrzxsony/nekome/refs/heads/main/Splash"
]

OUTPUT_FILE = "configs.json"  # Имя файла, куда сохранять результат в репозитории

def fetch_and_parse():
    all_configs = []
    
    for url in URLS:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8')
                
                # Пытаемся распарсить как JSON
                try:
                    data = json.loads(content)
                    if isinstance(data, list):
                        all_configs.extend(data)
                    elif isinstance(data, str):
                        all_configs.append(data)
                except json.JSONDecodeError:
                    # Если это обычный текст построчно
                    lines = content.splitlines()
                    for line in lines:
                        cleaned = line.strip().strip('"').strip("'")
                        if cleaned and not cleaned.startswith('#'):
                            all_configs.append(cleaned)
        except Exception as e:
            print(f"Ошибка при загрузке {url}: {e}")

    # Удаляем дубликаты, сохраняя исходный порядок
    unique_configs = list(dict.fromkeys(all_configs))
    return unique_configs

if __name__ == "__main__":
    configs = fetch_and_parse()
    print(f"Собрано уникальных конфигураций: {len(configs)}")
    
    if configs:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(configs, f, indent=4, ensure_ascii=False)
        print(f"Конфигурации успешно сохранены в {OUTPUT_FILE}")
    else:
        print("Конфигурации не найдены, файл не обновлен.")
