
# metaseq.py

MQOファイルを編集することに特化したプログラムです．（まだオブジェクトの形状などを編集できません．

load → 操作 → save した場合に，

- 未サポートの属性もそのまま維持されます
- 変更した要素以外にdiffが出ません(改行，インデント含めて)
- ScriptRunner.py でメタセコイア組み込みのPython用に書かれたスクリプトを実行できます

## ScriptRunner.py

```
usage: python ScriptRunner.py [-o OUTPUT.mqo] INPUT.mqo SCRIPT.py [SCRIPT2.py ...]
      -o OUTPUT.mqo Output file path. (Default out.mqo)
      INPUT.mqo Input file path. (Default in.mqo)
      SCRIPT[1...n].mqo Metasequoia Python script.
```


メタセコイア向けに書かれたスクリプトの一部機能を実行できます(対応してない機能多いです)．

たとえば，メタセコイアをインストールしたディレクトリにある `camera.py` を実行するには下記のように呼び出します．

```
python ScriptRunner.py sample.mqo "C:\Program Files\tetraface\Metasequoia4\Script\camera.py"
```

sample.mqoを読み込み，カメラの位置などを表示し，カメラ位置変更後のファイルが out.mqo に保存されます．


## gen_metaseq.rb

metaseq.pyを生成するRubyスクリプトです．metaseq.pyは元々Rubyで作っていたツールをもとにしているためRubyです．


## Library API

T.B.D.

## TODO:

- Object編集
- gen_metaseqをPythonに

## License


MIT License




