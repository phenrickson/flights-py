from sklearn.model_selection import train_test_split

# function to create train/valid/test splits
def create_train_val_test_split(
    data, stratify_col, test_size=0.2, val_size=0.25, random_seed=42
):
    # split data into train_val and test stratifying by column
    train_val, test = train_test_split(
        data, test_size=test_size, stratify=data[stratify_col], random_state=random_seed
    )

    # Then, split train_val into train and validation
    train, validation = train_test_split(
        train_val,
        test_size=val_size,
        stratify=train_val[stratify_col],
        random_state=random_seed,
    )
    return train, validation, test