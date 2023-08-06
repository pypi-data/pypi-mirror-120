# 更多用法，看文档
import typer

# 实例一下
app = typer.Typer()


# 加到命令组中 hello
@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")


# 加到命令组中 goodbye 接收 一个必要参数name, --formal 可修改默认值参数
@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")

