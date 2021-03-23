def generate_insert(table, table_name, ignore=False):
    df_list = table.values.tolist()

    insert_str = (f"INSERT INTO {table_name} (", f"INSERT IGNORE INTO {table_name} (")[ignore]
    for label in table.columns:
        if label != table.columns[-1]:
            insert_str += f"{label},"
        else:
            insert_str += f"{label})"

    insert_str += " VALUES "

    for ii in range(len(df_list)):
        row = df_list[ii]
        insert_str += "("
        for jj in range(len(row)):
            value = row[jj]
            if isinstance(value, str):
                for char in ["'", '"']:
                    value = value.replace(char, "")
                insert_str += f"'{value}'"
            else:
                insert_str += f"{value}"
            if ii == len(df_list) - 1 and jj == len(row) - 1:
                insert_str += ");"
            elif jj == len(row) - 1:
                insert_str += "),"
            else:
                insert_str += ","
    return insert_str