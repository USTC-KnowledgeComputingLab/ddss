import {
    Sequelize,
    DataTypes,
    Model,
    type InferAttributes,
    type InferCreationAttributes,
    type CreationOptional,
    type ModelStatic,
} from "sequelize";

// 定义基础模型类
class Fact extends Model<InferAttributes<Fact>, InferCreationAttributes<Fact>> {
    declare id: CreationOptional<number>;
    declare data: string;
}

class Idea extends Model<InferAttributes<Idea>, InferCreationAttributes<Idea>> {
    declare id: CreationOptional<number>;
    declare data: string;
}

export { Fact, Idea };

export async function initializeDatabase(addr: string): Promise<Sequelize> {
    // 转换地址：Python 的 sqlite:///path 转为 Sequelize 的 sqlite:path
    let sequelizeAddr = addr;
    if (addr.startsWith("sqlite:///")) {
        sequelizeAddr = `sqlite:${addr.replace("sqlite:///", "")}`;
    }

    const sequelize = new Sequelize(sequelizeAddr, {
        logging: false,
        define: {
            timestamps: false, // 去掉 createdAt 和 updatedAt
        },
    });

    Fact.init(
        {
            id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
            data: { type: DataTypes.TEXT, unique: true, allowNull: false },
        },
        { sequelize, tableName: "facts" },
    );

    Idea.init(
        {
            id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
            data: { type: DataTypes.TEXT, unique: true, allowNull: false },
        },
        { sequelize, tableName: "ideas" },
    );

    await sequelize.sync();
    return sequelize;
}

/**
 * 对应 Python 中的 insert_or_ignore。
 * Sequelize 的 bulkCreate 配合 ignoreDuplicates 可以实现跨方言的“重复则跳过”。
 */
export async function insertOrIgnore(model: ModelStatic<any>, data: string): Promise<void> {
    try {
        await model.bulkCreate([{ data } as any], {
            ignoreDuplicates: true,
        });
    } catch (error) {
        // 忽略重复键错误
    }
}
