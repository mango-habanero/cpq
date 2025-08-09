export const toSnakeCase = <T extends object>(
    obj: T
): Record<string, unknown> => {
    if (obj === null || typeof obj !== 'object')
        return obj as Record<string, unknown>;

    return Object.keys(obj).reduce(
        (acc, key) => {
            const snakeKey = key.replace(
                /[A-Z]/g,
                (letter) => `_${letter.toLowerCase()}`
            );
            const value = (obj as Record<string, unknown>)[key];

            acc[snakeKey] =
                value instanceof Date
                    ? value.toISOString()
                    : typeof value === 'object' && value !== null
                      ? toSnakeCase(value)
                      : value;
            return acc;
        },
        {} as Record<string, unknown>
    );
};
