CREATE TABLE IF NOT EXISTS user_settings (
user_id INT PRIMARY KEY,
user_lang VARCHAR(8) NOT NULL DEFAULT "ru",
user_prompts INT NOT NULL DEFAULT 3
)