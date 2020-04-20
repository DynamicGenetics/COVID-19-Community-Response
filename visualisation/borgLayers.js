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
        "category": "Factors affecting data quality",
        "colorsReversed": false,
        "displayOrder": 3
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
                            "#ffffe5"
                        ],
                        [
                            3.9205301236250003,
                            "#f7fcb9"
                        ],
                        [
                            3.96559556325,
                            "#d9f0a3"
                        ],
                        [
                            4.010661002875,
                            "#addd8e"
                        ],
                        [
                            4.0557264425,
                            "#78c679"
                        ],
                        [
                            4.100791882125,
                            "#41ab5d"
                        ],
                        [
                            4.145857321749999,
                            "#238443"
                        ],
                        [
                            4.190922761375,
                            "#006837"
                        ],
                        [
                            4.235988201,
                            "#004529"
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
        "colorsReversed": false,
        "displayOrder": 0
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
        "colorsReversed": false,
        "displayOrder": 0
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
                            "#ffffe5"
                        ],
                        [
                            3.6942312732451155e-05,
                            "#f7fcb9"
                        ],
                        [
                            5.431540914678513e-05,
                            "#d9f0a3"
                        ],
                        [
                            7.16885055611191e-05,
                            "#addd8e"
                        ],
                        [
                            8.906160197545308e-05,
                            "#78c679"
                        ],
                        [
                            0.00010643469838978706,
                            "#41ab5d"
                        ],
                        [
                            0.000123807794804121,
                            "#238443"
                        ],
                        [
                            0.000141180891218455,
                            "#006837"
                        ],
                        [
                            0.00015855398763278897,
                            "#004529"
                        ]
                    ]
                },
                "fill-opacity": 0.25
            },
            source: "groupCount_pop",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Community support groups (PP)",
        ref: "../data/groupCount.geojson",
        shownByDefault: true,
        "category": "Community support",
        "colorsReversed": false,
        "displayOrder": 0
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
                            "#ffffe5"
                        ],
                        [
                            0.24852157643229572,
                            "#f7fcb9"
                        ],
                        [
                            0.3558756369419678,
                            "#d9f0a3"
                        ],
                        [
                            0.4632296974516398,
                            "#addd8e"
                        ],
                        [
                            0.5705837579613119,
                            "#78c679"
                        ],
                        [
                            0.6779378184709839,
                            "#41ab5d"
                        ],
                        [
                            0.7852918789806559,
                            "#238443"
                        ],
                        [
                            0.892645939490328,
                            "#006837"
                        ],
                        [
                            1.0,
                            "#004529"
                        ]
                    ]
                },
                "fill-opacity": 0.25
            },
            source: "tweets_per_pop",
            type: "fill",
            "ID_name": null
        },
        name: "Support related tweets (PP)",
        ref: "../data/twitter_count.geojson",
        shownByDefault: true,
        "category": "Community support",
        "colorsReversed": false,
        "displayOrder": 0
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
                            "#fff7f3"
                        ],
                        [
                            12.375,
                            "#fde0dd"
                        ],
                        [
                            19.75,
                            "#fcc5c0"
                        ],
                        [
                            27.125,
                            "#fa9fb5"
                        ],
                        [
                            34.5,
                            "#f768a1"
                        ],
                        [
                            41.875,
                            "#dd3497"
                        ],
                        [
                            49.25,
                            "#ae017e"
                        ],
                        [
                            56.625,
                            "#7a0177"
                        ],
                        [
                            64.0,
                            "#49006a"
                        ]
                    ]
                },
                "fill-opacity": 0.5
            },
            source: "deprivation_30",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Multiple deprivation",
        ref: "../data/community_cohesion_deprivation.geojson",
        shownByDefault: false,
        "category": "Demographics",
        "colorsReversed": false,
        "displayOrder": 2
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
                            "#fff7f3"
                        ],
                        [
                            345.55,
                            "#fde0dd"
                        ],
                        [
                            665.5,
                            "#fcc5c0"
                        ],
                        [
                            985.4499999999999,
                            "#fa9fb5"
                        ],
                        [
                            1305.3999999999999,
                            "#f768a1"
                        ],
                        [
                            1625.35,
                            "#dd3497"
                        ],
                        [
                            1945.2999999999997,
                            "#ae017e"
                        ],
                        [
                            2265.25,
                            "#7a0177"
                        ],
                        [
                            2585.2,
                            "#49006a"
                        ]
                    ]
                },
                "fill-opacity": 0.5
            },
            source: "pop_density",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Population density",
        ref: "../data/covid_vulnerable.geojson",
        shownByDefault: false,
        "category": "Demographics",
        "colorsReversed": false,
        "displayOrder": 2
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
                            "#fff7ec"
                        ],
                        [
                            34.512499999999996,
                            "#fee8c8"
                        ],
                        [
                            36.724999999999994,
                            "#fdd49e"
                        ],
                        [
                            38.9375,
                            "#fdbb84"
                        ],
                        [
                            41.15,
                            "#fc8d59"
                        ],
                        [
                            43.3625,
                            "#ef6548"
                        ],
                        [
                            45.575,
                            "#d7301f"
                        ],
                        [
                            47.7875,
                            "#b30000"
                        ],
                        [
                            50.0,
                            "#7f0000"
                        ]
                    ]
                },
                "fill-opacity": 0.3333333333333333
            },
            source: "vulnerable_pct",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "COVID vulnerable (comorbidity %)",
        ref: "../data/covid_vulnerable.geojson",
        shownByDefault: false,
        "category": "COVID vulnerability",
        "colorsReversed": false,
        "displayOrder": 1
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
                            "#fff7ec"
                        ],
                        [
                            15.762653515,
                            "#fee8c8"
                        ],
                        [
                            17.43078901,
                            "#fdd49e"
                        ],
                        [
                            19.098924505,
                            "#fdbb84"
                        ],
                        [
                            20.76706,
                            "#fc8d59"
                        ],
                        [
                            22.435195495000002,
                            "#ef6548"
                        ],
                        [
                            24.10333099,
                            "#d7301f"
                        ],
                        [
                            25.771466484999998,
                            "#b30000"
                        ],
                        [
                            27.43960198,
                            "#7f0000"
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
        "colorsReversed": false,
        "displayOrder": 1
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
                            "#fff7ec"
                        ],
                        [
                            84.15,
                            "#fee8c8"
                        ],
                        [
                            125.8,
                            "#fdd49e"
                        ],
                        [
                            167.45,
                            "#fdbb84"
                        ],
                        [
                            209.1,
                            "#fc8d59"
                        ],
                        [
                            250.75,
                            "#ef6548"
                        ],
                        [
                            292.4,
                            "#d7301f"
                        ],
                        [
                            334.05,
                            "#b30000"
                        ],
                        [
                            375.7,
                            "#7f0000"
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
        "colorsReversed": false,
        "displayOrder": 1
    }
]