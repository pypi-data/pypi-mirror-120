Example config
```
[Elastic]
index = dyn_test
doc_type = df
```

<h2>Change logs</h2>

*  0.1.0
    1) use elastic base model
    2) change function args <b>add_els_config</b>
    <pre>
    def add_els_config(self, index, doc_type):
        self.index = index
        self.doc_type = doc_type
    </pre>
