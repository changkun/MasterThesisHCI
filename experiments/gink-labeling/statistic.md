# Pilot Study

## Total numbers

Total participants

```m
> db.supervised.distinct('email');
[
        "bastisteer@t-online.de",
        "hi@changkun.us",
        "jupame@p-z-meyer.de",
        "fe.buchner@t-online.de"
]
> db.supervised.find({email: 'bastisteer@t-online.de'}).count();
1
> db.supervised.find({email: 'jupame@p-z-meyer.de'}).count();
15
> db.supervised.find({email: 'fe.buchner@t-online.de'}).count();
47
> db.supervised.find({email: 'hi@changkun.us'}).count();
12
> db.supervised.find({}).count();
104
```

## Age distribution

```m
> db.supervised.distinct('age')
[ 28, 25, 20 ]
```

## Raw Dataset

![supervised.json](./supervised.json)