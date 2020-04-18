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
                            "#fff7ec"
                        ],
                        [
                            13.399999999999999,
                            "#fee8c8"
                        ],
                        [
                            20.099999999999998,
                            "#fdd49e"
                        ],
                        [
                            26.799999999999997,
                            "#fdbb84"
                        ],
                        [
                            33.5,
                            "#fc8d59"
                        ],
                        [
                            40.199999999999996,
                            "#ef6548"
                        ],
                        [
                            46.89999999999999,
                            "#d7301f"
                        ],
                        [
                            53.599999999999994,
                            "#b30000"
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
        shownByDefault: false
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
                            "#ffffe5"
                        ],
                        [
                            0.08011633711111098,
                            "#f7fcb9"
                        ],
                        [
                            0.12017450566666646,
                            "#d9f0a3"
                        ],
                        [
                            0.16023267422222195,
                            "#addd8e"
                        ],
                        [
                            0.20029084277777745,
                            "#78c679"
                        ],
                        [
                            0.24034901133333292,
                            "#41ab5d"
                        ],
                        [
                            0.2804071798888884,
                            "#238443"
                        ],
                        [
                            0.3204653484444439,
                            "#006837"
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
        shownByDefault: false
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
                            "#ffffe5"
                        ],
                        [
                            13.11111111111111,
                            "#f7fcb9"
                        ],
                        [
                            19.666666666666664,
                            "#d9f0a3"
                        ],
                        [
                            26.22222222222222,
                            "#addd8e"
                        ],
                        [
                            32.77777777777778,
                            "#78c679"
                        ],
                        [
                            39.33333333333333,
                            "#41ab5d"
                        ],
                        [
                            45.888888888888886,
                            "#238443"
                        ],
                        [
                            52.44444444444444,
                            "#006837"
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
        shownByDefault: false
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
                            "#084081"
                        ],
                        [
                            3.933333333333334,
                            "#e0f3db"
                        ],
                        [
                            5.900000000000001,
                            "#2b8cbe"
                        ],
                        [
                            7.866666666666668,
                            "#a8ddb5"
                        ],
                        [
                            9.833333333333336,
                            "#7bccc4"
                        ],
                        [
                            11.800000000000002,
                            "#4eb3d3"
                        ],
                        [
                            13.76666666666667,
                            "#ccebc5"
                        ],
                        [
                            15.733333333333336,
                            "#0868ac"
                        ]
                    ]
                },
                "fill-opacity": 0.5
            },
            source: "vulnerable_pct",
            type: "fill"
        },
        name: "Vulnerable (% with >=1 comorbidity)",
        ref: "../data/covid_vulnerable.geojson",
        shownByDefault: false
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
                            "#084081"
                        ],
                        [
                            568.8,
                            "#e0f3db"
                        ],
                        [
                            853.1999999999999,
                            "#2b8cbe"
                        ],
                        [
                            1137.6,
                            "#a8ddb5"
                        ],
                        [
                            1422.0,
                            "#7bccc4"
                        ],
                        [
                            1706.3999999999999,
                            "#4eb3d3"
                        ],
                        [
                            1990.7999999999997,
                            "#ccebc5"
                        ],
                        [
                            2275.2,
                            "#0868ac"
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
        shownByDefault: false
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
                            "#084081"
                        ],
                        [
                            2.965574213333333,
                            "#e0f3db"
                        ],
                        [
                            4.448361319999999,
                            "#2b8cbe"
                        ],
                        [
                            5.931148426666666,
                            "#a8ddb5"
                        ],
                        [
                            7.4139355333333326,
                            "#7bccc4"
                        ],
                        [
                            8.896722639999998,
                            "#4eb3d3"
                        ],
                        [
                            10.379509746666665,
                            "#ccebc5"
                        ],
                        [
                            11.862296853333332,
                            "#0868ac"
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
        shownByDefault: false
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
                            "#084081"
                        ],
                        [
                            74.04444444444444,
                            "#e0f3db"
                        ],
                        [
                            111.06666666666666,
                            "#2b8cbe"
                        ],
                        [
                            148.08888888888887,
                            "#a8ddb5"
                        ],
                        [
                            185.1111111111111,
                            "#7bccc4"
                        ],
                        [
                            222.13333333333333,
                            "#4eb3d3"
                        ],
                        [
                            259.1555555555555,
                            "#ccebc5"
                        ],
                        [
                            296.17777777777775,
                            "#0868ac"
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
        shownByDefault: false
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
                            "#004529"
                        ],
                        [
                            6.035108449310647e-05,
                            "#f7fcb9"
                        ],
                        [
                            9.052662673965972e-05,
                            "#238443"
                        ],
                        [
                            0.00012070216898621295,
                            "#addd8e"
                        ],
                        [
                            0.00015087771123276618,
                            "#78c679"
                        ],
                        [
                            0.00018105325347931943,
                            "#41ab5d"
                        ],
                        [
                            0.00021122879572587266,
                            "#d9f0a3"
                        ],
                        [
                            0.0002414043379724259,
                            "#006837"
                        ]
                    ]
                },
                "fill-opacity": 0.3333333333333333
            },
            source: "groupCount_pop",
            type: "fill"
        },
        name: "Community support groups (per capita)",
        ref: "../data/groupCount.geojson",
        shownByDefault: false
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
        shownByDefault: false
    }
]