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
                            4.8,
                            "#f7fcf0"
                        ],
                        [
                            12.337499999999999,
                            "#e0f3db"
                        ],
                        [
                            19.875,
                            "#ccebc5"
                        ],
                        [
                            27.412499999999998,
                            "#a8ddb5"
                        ],
                        [
                            34.949999999999996,
                            "#7bccc4"
                        ],
                        [
                            42.4875,
                            "#4eb3d3"
                        ],
                        [
                            50.02499999999999,
                            "#2b8cbe"
                        ],
                        [
                            57.56249999999999,
                            "#0868ac"
                        ],
                        [
                            65.1,
                            "#084081"
                        ]
                    ]
                },
                "fill-opacity": 1.0
            },
            source: "language",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Welsh language use",
        ref: "../data/bias_language.geojson",
        shownByDefault: false,
        "category": "Risk of bias in our sources",
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
                            3.875464684,
                            "#7f0000"
                        ],
                        [
                            3.9205301236250003,
                            "#b30000"
                        ],
                        [
                            3.96559556325,
                            "#d7301f"
                        ],
                        [
                            4.010661002875,
                            "#ef6548"
                        ],
                        [
                            4.0557264425,
                            "#fc8d59"
                        ],
                        [
                            4.100791882125,
                            "#fdbb84"
                        ],
                        [
                            4.145857321749999,
                            "#fdd49e"
                        ],
                        [
                            4.190922761375,
                            "#fee8c8"
                        ],
                        [
                            4.235988201,
                            "#fff7ec"
                        ]
                    ]
                },
                "fill-opacity": 0.25
            },
            source: "communityCohesion",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Community cohesion",
        ref: "../data/community_cohesion_deprivation.geojson",
        shownByDefault: false,
        "category": "Community support",
        "colorsReversed": true
    },
    {
        layerSpec: {
            id: "groups",
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
            source: "groups",
            type: "circle",
            "ID_name": null
        },
        name: "Community support groups",
        ref: "../data/groups.geojson",
        shownByDefault: true,
        "category": "Community support",
        "colorsReversed": false
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
                            1.9569216318117182e-05,
                            "#fff7ec"
                        ],
                        [
                            3.6942312732451155e-05,
                            "#fee8c8"
                        ],
                        [
                            5.431540914678513e-05,
                            "#fdd49e"
                        ],
                        [
                            7.16885055611191e-05,
                            "#fdbb84"
                        ],
                        [
                            8.906160197545308e-05,
                            "#fc8d59"
                        ],
                        [
                            0.00010643469838978706,
                            "#ef6548"
                        ],
                        [
                            0.000123807794804121,
                            "#d7301f"
                        ],
                        [
                            0.000141180891218455,
                            "#b30000"
                        ],
                        [
                            0.00015855398763278897,
                            "#7f0000"
                        ]
                    ]
                },
                "fill-opacity": 0.25
            },
            source: "groupCount_pop",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Community support groups (per population)",
        ref: "../data/groupCount.geojson",
        shownByDefault: true,
        "category": "Community support",
        "colorsReversed": false
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
                            0.1411675159226237,
                            "#fff7ec"
                        ],
                        [
                            0.24852157643229572,
                            "#fee8c8"
                        ],
                        [
                            0.3558756369419678,
                            "#fdd49e"
                        ],
                        [
                            0.4632296974516398,
                            "#fdbb84"
                        ],
                        [
                            0.5705837579613119,
                            "#fc8d59"
                        ],
                        [
                            0.6779378184709839,
                            "#ef6548"
                        ],
                        [
                            0.7852918789806559,
                            "#d7301f"
                        ],
                        [
                            0.892645939490328,
                            "#b30000"
                        ],
                        [
                            1.0,
                            "#7f0000"
                        ]
                    ]
                },
                "fill-opacity": 0.25
            },
            source: "tweets_per_pop",
            type: "fill",
            "ID_name": null
        },
        name: "Support related tweets (per population)",
        ref: "../data/twitter_count.geojson",
        shownByDefault: true,
        "category": "Community support",
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
                            5.0,
                            "#ffffe5"
                        ],
                        [
                            12.375,
                            "#f7fcb9"
                        ],
                        [
                            19.75,
                            "#d9f0a3"
                        ],
                        [
                            27.125,
                            "#addd8e"
                        ],
                        [
                            34.5,
                            "#78c679"
                        ],
                        [
                            41.875,
                            "#41ab5d"
                        ],
                        [
                            49.25,
                            "#238443"
                        ],
                        [
                            56.625,
                            "#006837"
                        ],
                        [
                            64.0,
                            "#004529"
                        ]
                    ]
                },
                "fill-opacity": 0.3333333333333333
            },
            source: "deprivation_30",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Multiple deprivation",
        ref: "../data/community_cohesion_deprivation.geojson",
        shownByDefault: false,
        "category": "Demographics",
        "colorsReversed": false
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
                            25.6,
                            "#ffffe5"
                        ],
                        [
                            345.55,
                            "#f7fcb9"
                        ],
                        [
                            665.5,
                            "#d9f0a3"
                        ],
                        [
                            985.4499999999999,
                            "#addd8e"
                        ],
                        [
                            1305.3999999999999,
                            "#78c679"
                        ],
                        [
                            1625.35,
                            "#41ab5d"
                        ],
                        [
                            1945.2999999999997,
                            "#238443"
                        ],
                        [
                            2265.25,
                            "#006837"
                        ],
                        [
                            2585.2,
                            "#004529"
                        ]
                    ]
                },
                "fill-opacity": 0.3333333333333333
            },
            source: "pop_density",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Population density",
        ref: "../data/covid_vulnerable.geojson",
        shownByDefault: false,
        "category": "Demographics",
        "colorsReversed": false
    },
    {
        layerSpec: {
            filter: [
                "==",
                "$type",
                "Polygon"
            ],
            id: "pop",
            paint: {
                "fill-color": {
                    property: "pop",
                    stops: [
                        [
                            60183.0,
                            "#ffffe5"
                        ],
                        [
                            98191.125,
                            "#f7fcb9"
                        ],
                        [
                            136199.25,
                            "#d9f0a3"
                        ],
                        [
                            174207.375,
                            "#addd8e"
                        ],
                        [
                            212215.5,
                            "#78c679"
                        ],
                        [
                            250223.625,
                            "#41ab5d"
                        ],
                        [
                            288231.75,
                            "#238443"
                        ],
                        [
                            326239.875,
                            "#006837"
                        ],
                        [
                            364248.0,
                            "#004529"
                        ]
                    ]
                },
                "fill-opacity": 0.3333333333333333
            },
            source: "pop",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Population",
        ref: "../data/covid_vulnerable.geojson",
        shownByDefault: false,
        "category": "Demographics",
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
                            32.3,
                            "#fff7f3"
                        ],
                        [
                            34.512499999999996,
                            "#fde0dd"
                        ],
                        [
                            36.724999999999994,
                            "#fcc5c0"
                        ],
                        [
                            38.9375,
                            "#fa9fb5"
                        ],
                        [
                            41.15,
                            "#f768a1"
                        ],
                        [
                            43.3625,
                            "#dd3497"
                        ],
                        [
                            45.575,
                            "#ae017e"
                        ],
                        [
                            47.7875,
                            "#7a0177"
                        ],
                        [
                            50.0,
                            "#49006a"
                        ]
                    ]
                },
                "fill-opacity": 0.3333333333333333
            },
            source: "vulnerable_pct",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "COVID vulnerable (comobidity %)",
        ref: "../data/covid_vulnerable.geojson",
        shownByDefault: false,
        "category": "COVID vulnerability",
        "colorsReversed": false
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
                            14.09451802,
                            "#fff7f3"
                        ],
                        [
                            15.762653515,
                            "#fde0dd"
                        ],
                        [
                            17.43078901,
                            "#fcc5c0"
                        ],
                        [
                            19.098924505,
                            "#fa9fb5"
                        ],
                        [
                            20.76706,
                            "#f768a1"
                        ],
                        [
                            22.435195495000002,
                            "#dd3497"
                        ],
                        [
                            24.10333099,
                            "#ae017e"
                        ],
                        [
                            25.771466484999998,
                            "#7a0177"
                        ],
                        [
                            27.43960198,
                            "#49006a"
                        ]
                    ]
                },
                "fill-opacity": 0.3333333333333333
            },
            source: "pop_elderly",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Elderly population (% over 65)",
        ref: "../data/covid_vulnerable.geojson",
        shownByDefault: false,
        "category": "COVID vulnerability",
        "colorsReversed": false
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
                            42.5,
                            "#fff7f3"
                        ],
                        [
                            84.15,
                            "#fde0dd"
                        ],
                        [
                            125.8,
                            "#fcc5c0"
                        ],
                        [
                            167.45,
                            "#fa9fb5"
                        ],
                        [
                            209.1,
                            "#f768a1"
                        ],
                        [
                            250.75,
                            "#dd3497"
                        ],
                        [
                            292.4,
                            "#ae017e"
                        ],
                        [
                            334.05,
                            "#7a0177"
                        ],
                        [
                            375.7,
                            "#49006a"
                        ]
                    ]
                },
                "fill-opacity": 0.3333333333333333
            },
            source: "covid_per100k",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "COVID cases (per 100k)",
        ref: "../data/covid_cases.geojson",
        shownByDefault: false,
        "category": "COVID vulnerability",
        "colorsReversed": false
    }
]