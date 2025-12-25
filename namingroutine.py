def Initialize():

    # Essential Lists for CMD plotting and labeling models

    dictevoltracmasses = {0: '.80', 1: '.82', 2: '.84', 3: '.86', 4: '.88'}
    dictevoltracmassesspelled = {0: 'df0080', 1: 'df008200', 2: 'df008400', 3: 'df008600', 4: 'df008800'}
    dictwdmasses = {0: '.54', 1: '.61', 2: '.68', 3: '.77', 4: '.87', 5: '1.00', 6: '1.10'}

    dictisoages = {0: '9000', 1: '10000', 2: '11000', 3: '12000'}
    dictisoagesspelled = {0: 'df9000', 1: 'df10000', 2: 'df11000', 3: 'df12000'}

    dictfilters = {0: '275', 1: '336', 2: '438', 3: '606', 4: '814'}
    dictfiltermagnames = {0: '\(m_{F275W} \)', 1: '\(m_{F336W} \)', 2: '\(m_{F438W} \)', 3: '\(m_{F606W} \)', 4: '\(m_{F814W} \)'}

    allfilters = ["F275W","F336W","F438W","F606W","F814W"]

    colors = [
        'green', 'deeppink', 'dodgerblue', 'orange', 'teal', 'darkkhaki',
        'magenta', 'rosybrown', 'crimson',
        'steelblue', 'darkorange', 'red', 'blue', 'limegreen', 'gold',
        'salmon', 'mediumseagreen', 'turquoise', 'slateblue', 'orchid', 'firebrick',
        'peru', 'hotpink', 'olive', 'mediumvioletred',
        'cornflowerblue', 'tomato', 'darkcyan', 'darkslateblue', 'lightsteelblue'
    ]

    return locals()