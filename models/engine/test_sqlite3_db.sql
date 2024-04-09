PRAGMA foreign_keys=OFF;

BEGIN TRANSACTION;

CREATE TABLE `countries` (
    `country_id` INTEGER PRIMARY KEY,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `name` TEXT NOT NULL,
    `type` TEXT NOT NULL
);

CREATE TABLE `users` (
    `user_id` INTEGER PRIMARY KEY,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `username` TEXT,
    `first_name` TEXT,
    `balance` INTEGER,
    `referrer_id` INTEGER,
    `ongoing_order` TEXT
);


CREATE TABLE `proxy_configs` (
    `proxy_config_id` TEXT PRIMARY KEY,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `provider` TEXT,
    `country_id` INTEGER,
    `country` TEXT,
    `provider_id` INTEGER,
    `period` TEXT
);
CREATE TABLE `periods` (
    `period_id` TEXT PRIMARY KEY,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `name` TEXT,
    `price` INTEGER
);

CREATE TABLE `orders` (
    `order_id` TEXT PRIMARY KEY,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `user_id` INTEGER,
    `provider` TEXT,
    `provider_id` INTEGER,
    `amount_paid` INTEGER,
    `rental_period` TEXT,
    `item_delivered` TEXT
);

CREATE TABLE `deposits` (
    `tx_id` TEXT PRIMARY KEY,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `user_id` INTEGER NOT NULL,
    `address` TEXT NOT NULL,
    `crypto` TEXT NOT NULL,
    `amount` INTEGER NOT NULL
);

COMMIT;
