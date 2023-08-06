#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author jsbxyyx
if __name__ is not None and "." in __name__:
    from .mysql_base import MySqlBase, MysqlStatementVisitor, MysqlOutputVisitor
else:
    from am.mysql_base import MySqlBase, MysqlStatementVisitor, MysqlOutputVisitor


def test_sql():
    select_sql = """
        select * from test where name = ? and id = ?;
        select * from test where name = ? and id = ? order by t.id asc, t.name desc limit 10, 0 for update;
        """
    ss = MySqlBase.parserSQLStatement(select_sql)
    for idx in range(len(ss)):
        s = MysqlStatementVisitor().visit(ss[idx])
        output = list()
        MysqlOutputVisitor().visitSelectStatement(s, output)
        string = ''.join(output)
        print(string)
        print('*' * 100)

    insert_sql = """
        insert into test(id, name) values(?,?), (?,?), (?, 1), (?, '1'), (?, 1.1);
        insert into test(id, name) values(?,now());
        insert into test(id, name) values(null,now());
        """
    ss = MySqlBase.parserSQLStatement(insert_sql)
    for idx in range(len(ss)):
        s = MysqlStatementVisitor().visit(ss[idx])
        output = list()
        MysqlOutputVisitor().visitInsertStatement(s, output)
        string = ''.join(output)
        print(string)
        print('*' * 100)

    update_sql = """
        update test t set t.id = ?, name = ? where t.id in (?,?) and t.like like '%1%';
        update test t set t.id = ?, name = ? where t.id in (?,?) and t.id is null;
        update test t set t.id = ?, name = ? where t.id in (?,?) and t.like like '%1%' order by t.id, t.name desc limit 1;
        """
    ss = MySqlBase.parserSQLStatement(update_sql)
    for idx in range(len(ss)):
        s = MysqlStatementVisitor().visit(ss[idx])
        output = list()
        MysqlOutputVisitor().visitUpdateStatement(s, output)
        string = ''.join(output)
        print(string)
        print('*' * 100)

    delete_sql = """
        delete t from test t where t.id = ? and t.name in (?,?);
        delete t from test t where t.id between 10 and 30 and t.name = '';
        delete t from test t where t.id between 10 and 30 and t.name = '' order by t1.name desc limit 1;
        delete t from test t where t.name = 0x1 and t.name = x'11' and t.name = b'1' order by t1.name desc limit 1;
        delete t from test t where t.name = format(1.23, 1) and t.created = date_format( now(), '%Y%m%d');
        """
    ss = MySqlBase.parserSQLStatement(delete_sql)
    for idx in range(len(ss)):
        s = MysqlStatementVisitor().visit(ss[idx])
        output = list()
        MysqlOutputVisitor().visitDeleteStatement(s, output)
        string = ''.join(output)
        print(string)
        print('*' * 100)

    sql = """
        insert into test values(%(user_id)s, %(count)s);
        """
    ss = MySqlBase.parserSQLStatement(sql)
    for idx in range(len(ss)):
        s = MysqlStatementVisitor().visit(ss[idx])
        output = list()
        MysqlOutputVisitor().visitInsertStatement(s, output)
        string = ''.join(output)
        print(string)
        print('*' * 100)

    print()


if __name__ == '__main__':
    test_sql()
