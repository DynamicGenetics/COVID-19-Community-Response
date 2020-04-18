var layers=[
    {
        layerSpec: {
            filter: [
                "==",
                "$type",
                "Polygon"
            ],
            id: "language",
            paint: {
                "fill-color": {
                    property: "language",
                    stops: [
                        [
                            6.699999999999999,
                            "#f7fcf0"
                        ],
                        [
                            13.399999999999999,
                            "#e0f3db"
                        ],
                        [
                            20.099999999999998,
                            "#ccebc5"
                        ],
                        [
                            26.799999999999997,
                            "#a8ddb5"
                        ],
                        [
                            33.5,
                            "#7bccc4"
                        ],
                        [
                            40.199999999999996,
                            "#4eb3d3"
                        ],
                        [
                            46.89999999999999,
                            "#2b8cbe"
                        ],
                        [
                            53.599999999999994,
                            "#0868ac"
                        ],
                        [
                            60.3,
                            "#084081"
                        ]
                    ]
                },
                "fill-opacity": 0.5
            },
            source: "language",
            type: "fill"
        },
        name: "Welsh language use",
        ref: "../data/bias_language.geojson",
        shownByDefault: false,
        "category": "Bias",
        "colorsReversed": false
    },
    {
        layerSpec: {
            filter: [
                "==",
                "$type",
                "Polygon"
            ],
            id: "communityCohesion",
            paint: {
                "fill-color": {
                    property: "communityCohesion",
                    stops: [
                        [
                            0.04005816855555549,
                            "#fff7ec"
                        ],
                        [
                            0.08011633711111098,
                            "#fee8c8"
                        ],
                        [
                            0.12017450566666646,
                            "#fdd49e"
                        ],
                        [
                            0.16023267422222195,
                            "#fdbb84"
                        ],
                        [
                            0.20029084277777745,
                            "#fc8d59"
                        ],
                        [
                            0.24034901133333292,
                            "#ef6548"
                        ],
                        [
                            0.2804071798888884,
                            "#d7301f"
                        ],
                        [
                            0.3204653484444439,
                            "#b30000"
                        ],
                        [
                            0.3605235169999994,
                            "#7f0000"
                        ]
                    ]
                },
                "fill-opacity": 0.3333333333333333
            },
            source: "communityCohesion",
            type: "fill"
        },
        name: "Community cohesion",
        ref: "../data/community_cohesion_deprivation.geojson",
        shownByDefault: false,
        "category": "Community vulnerability",
        "colorsReversed": false
    },
    {
        layerSpec: {
            filter: [
                "==",
                "$type",
                "Polygon"
            ],
            id: "deprivation_30",
            paint: {
                "fill-color": {
                    property: "deprivation_30",
                    stops: [
                        [
                            6.555555555555555,
                            "#fff7ec"
                        ],
                        [
                            13.11111111111111,
                            "#fee8c8"
                        ],
                        [
                            19.666666666666664,
                            "#fdd49e"
                        ],
                        [
                            26.22222222222222,
                            "#fdbb84"
                        ],
                        [
                            32.77777777777778,
                            "#fc8d59"
                        ],
                        [
                            39.33333333333333,
                            "#ef6548"
                        ],
                        [
                            45.888888888888886,
                            "#d7301f"
                        ],
                        [
                            52.44444444444444,
                            "#b30000"
                        ],
                        [
                            59.0,
                            "#7f0000"
                        ]
                    ]
                },
                "fill-opacity": 0.3333333333333333
            },
            source: "deprivation_30",
            type: "fill"
        },
        name: "Multiple deprivation",
        ref: "../data/community_cohesion_deprivation.geojson",
        shownByDefault: false,
        "category": "Community vulnerability",
        "colorsReversed": false
    },
    {
        layerSpec: {
            filter: [
                "==",
                "$type",
                "Polygon"
            ],
            id: "vulnerable_pct",
            paint: {
                "fill-color": {
                    property: "vulnerable_pct",
                    stops: [
                        [
                            1.966666666666667,
                            "#004529"
                        ],
                        [
                            3.933333333333334,
                            "#006837"
                        ],
                        [
                            5.900000000000001,
                            "#238443"
                        ],
                        [
                            7.866666666666668,
                            "#41ab5d"
                        ],
                        [
                            9.833333333333336,
                            "#78c679"
                        ],
                        [
                            11.800000000000002,
                            "#addd8e"
                        ],
                        [
                            13.76666666666667,
                            "#d9f0a3"
                        ],
                        [
                            15.733333333333336,
                            "#f7fcb9"
                        ],
                        [
                            17.700000000000003,
                            "#ffffe5"
                        ]
                    ]
                },
                "fill-opacity": 0.5
            },
            source: "vulnerable_pct",
            type: "fill"
        },
        name: "Vulnerable (% with comorbidities)",
        ref: "../data/covid_vulnerable.geojson",
        shownByDefault: false,
        "category": "COVID vulnerability",
        "colorsReversed": true
    },
    {
        layerSpec: {
            filter: [
                "==",
                "$type",
                "Polygon"
            ],
            id: "pop_density",
            paint: {
                "fill-color": {
                    property: "pop_density",
                    stops: [
                        [
                            284.4,
                            "#004529"
                        ],
                        [
                            568.8,
                            "#006837"
                        ],
                        [
                            853.1999999999999,
                            "#238443"
                        ],
                        [
                            1137.6,
                            "#41ab5d"
                        ],
                        [
                            1422.0,
                            "#78c679"
                        ],
                        [
                            1706.3999999999999,
                            "#addd8e"
                        ],
                        [
                            1990.7999999999997,
                            "#d9f0a3"
                        ],
                        [
                            2275.2,
                            "#f7fcb9"
                        ],
                        [
                            2559.6,
                            "#ffffe5"
                        ]
                    ]
                },
                "fill-opacity": 0.5
            },
            source: "pop_density",
            type: "fill"
        },
        name: "Population density",
        ref: "../data/covid_vulnerable.geojson",
        shownByDefault: false,
        "category": "COVID vulnerability",
        "colorsReversed": true
    },
    {
        layerSpec: {
            filter: [
                "==",
                "$type",
                "Polygon"
            ],
            id: "pop_elderly",
            paint: {
                "fill-color": {
                    property: "pop_elderly",
                    stops: [
                        [
                            1.4827871066666665,
                            "#004529"
                        ],
                        [
                            2.965574213333333,
                            "#006837"
                        ],
                        [
                            4.448361319999999,
                            "#238443"
                        ],
                        [
                            5.931148426666666,
                            "#41ab5d"
                        ],
                        [
                            7.4139355333333326,
                            "#78c679"
                        ],
                        [
                            8.896722639999998,
                            "#addd8e"
                        ],
                        [
                            10.379509746666665,
                            "#d9f0a3"
                        ],
                        [
                            11.862296853333332,
                            "#f7fcb9"
                        ],
                        [
                            13.345083959999998,
                            "#ffffe5"
                        ]
                    ]
                },
                "fill-opacity": 0.5
            },
            source: "pop_elderly",
            type: "fill"
        },
        name: "Elderly population (% over 65)",
        ref: "../data/covid_vulnerable.geojson",
        shownByDefault: false,
        "category": "COVID vulnerability",
        "colorsReversed": true
    },
    {
        layerSpec: {
            filter: [
                "==",
                "$type",
                "Polygon"
            ],
            id: "covid_per100k",
            paint: {
                "fill-color": {
                    property: "covid_per100k",
                    stops: [
                        [
                            37.02222222222222,
                            "#004529"
                        ],
                        [
                            74.04444444444444,
                            "#006837"
                        ],
                        [
                            111.06666666666666,
                            "#238443"
                        ],
                        [
                            148.08888888888887,
                            "#41ab5d"
                        ],
                        [
                            185.1111111111111,
                            "#78c679"
                        ],
                        [
                            222.13333333333333,
                            "#addd8e"
                        ],
                        [
                            259.1555555555555,
                            "#d9f0a3"
                        ],
                        [
                            296.17777777777775,
                            "#f7fcb9"
                        ],
                        [
                            333.2,
                            "#ffffe5"
                        ]
                    ]
                },
                "fill-opacity": 0.5
            },
            source: "covid_per100k",
            type: "fill"
        },
        name: "COVID cases (per 100k)",
        ref: "../data/covid_cases.geojson",
        shownByDefault: false,
        "category": "COVID vulnerability",
        "colorsReversed": true
    },
    {
        layerSpec: {
            filter: [
                "==",
                "$type",
                "Polygon"
            ],
            id: "groupCount_pop",
            paint: {
                "fill-color": {
                    property: "groupCount_pop",
                    stops: [
                        [
                            3.0175542246553237e-05,
                            "#7f0000"
                        ],
                        [
                            6.035108449310647e-05,
                            "#b30000"
                        ],
                        [
                            9.052662673965972e-05,
                            "#d7301f"
                        ],
                        [
                            0.00012070216898621295,
                            "#ef6548"
                        ],
                        [
                            0.00015087771123276618,
                            "#fc8d59"
                        ],
                        [
                            0.00018105325347931943,
                            "#fdbb84"
                        ],
                        [
                            0.00021122879572587266,
                            "#fdd49e"
                        ],
                        [
                            0.0002414043379724259,
                            "#fee8c8"
                        ],
                        [
                            0.0002715798802189791,
                            "#fff7ec"
                        ]
                    ]
                },
                "fill-opacity": 0.3333333333333333
            },
            source: "groupCount_pop",
            type: "fill"
        },
        name: "Community support groups (per population)",
        ref: "../data/groupCount.geojson",
        shownByDefault: false,
        "category": "Community vulnerability",
        "colorsReversed": true
    },
    {
        layerSpec: {
            filter: [
                "==",
                "$type",
                "Polygon"
            ],
            id: "tweets_per_pop",
            paint: {
                "fill-color": {
                    property: "tweets_per_pop",
                    stops: [
                        [
                            0.09542583156415292,
                            "#084081"
                        ],
                        [
                            0.19085166312830584,
                            "#0868ac"
                        ],
                        [
                            0.2862774946924588,
                            "#2b8cbe"
                        ],
                        [
                            0.3817033262566117,
                            "#4eb3d3"
                        ],
                        [
                            0.4771291578207646,
                            "#7bccc4"
                        ],
                        [
                            0.5725549893849176,
                            "#a8ddb5"
                        ],
                        [
                            0.6679808209490704,
                            "#ccebc5"
                        ],
                        [
                            0.7634066525132234,
                            "#e0f3db"
                        ],
                        [
                            0.8588324840773763,
                            "#f7fcf0"
                        ]
                    ]
                },
                "fill-opacity": 0.5
            },
            source: "tweets_per_pop",
            type: "fill"
        },
        name: "Tweets (per population)",
        ref: "../data/twitter_count.geojson",
        shownByDefault: false,
        "category": "Bias",
        "colorsReversed": true
    },
    {
        layerSpec: {
            id: "groups_points",
            paint: {
                "circle-color": "#111",
                "circle-radius": {
                    base: 1.75,
                    stops: [
                        [
                            12,
                            2.7
                        ],
                        [
                            22,
                            180
                        ]
                    ]
                }
            },
            source: "groups_points",
            type: "circle"
        },
        name: "Community support groups",
        ref: "../data/groups.geojson",
        shownByDefault: false,
        "category": "Community vulnerability",
        "colorsReversed": true
    }
]