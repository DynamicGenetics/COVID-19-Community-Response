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
                            21.54455652324579,
                            "#e0f3db"
                        ],
                        [
                            38.28911304649158,
                            "#ccebc5"
                        ],
                        [
                            55.03366956973737,
                            "#a8ddb5"
                        ],
                        [
                            71.77822609298316,
                            "#7bccc4"
                        ],
                        [
                            88.52278261622895,
                            "#4eb3d3"
                        ],
                        [
                            105.26733913947474,
                            "#2b8cbe"
                        ],
                        [
                            122.01189566272053,
                            "#0868ac"
                        ],
                        [
                            138.75645218596634,
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
        ref: "data/bias_language.geojson",
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
                            3.9825299670663723,
                            "#f7fcb9"
                        ],
                        [
                            4.089595250132745,
                            "#d9f0a3"
                        ],
                        [
                            4.1966605331991165,
                            "#addd8e"
                        ],
                        [
                            4.303725816265489,
                            "#78c679"
                        ],
                        [
                            4.410791099331861,
                            "#41ab5d"
                        ],
                        [
                            4.517856382398233,
                            "#238443"
                        ],
                        [
                            4.624921665464605,
                            "#006837"
                        ],
                        [
                            4.731986948530977,
                            "#004529"
                        ]
                    ]
                },
                "fill-opacity": 0.3333333333333333
            },
            source: "communityCohesion",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Community cohesion",
        ref: "data/community_cohesion_deprivation.geojson",
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
        ref: "data/groups.geojson",
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
                            0.3351030713849671,
                            "#f7fcb9"
                        ],
                        [
                            0.5290386268473104,
                            "#d9f0a3"
                        ],
                        [
                            0.7229741823096537,
                            "#addd8e"
                        ],
                        [
                            0.9169097377719971,
                            "#78c679"
                        ],
                        [
                            1.1108452932343407,
                            "#41ab5d"
                        ],
                        [
                            1.3047808486966839,
                            "#238443"
                        ],
                        [
                            1.4987164041590273,
                            "#006837"
                        ],
                        [
                            1.6926519596213707,
                            "#004529"
                        ]
                    ]
                },
                "fill-opacity": 0.3333333333333333
            },
            source: "tweets_per_pop",
            type: "fill",
            "ID_name": null
        },
        name: "Support related tweets",
        ref: "data/twitter_count.geojson",
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
                            37.14676220750553,
                            "#fee8c8"
                        ],
                        [
                            41.993524415011066,
                            "#fdd49e"
                        ],
                        [
                            46.840286622516594,
                            "#fdbb84"
                        ],
                        [
                            51.68704883002213,
                            "#fc8d59"
                        ],
                        [
                            56.53381103752766,
                            "#ef6548"
                        ],
                        [
                            61.38057324503319,
                            "#d7301f"
                        ],
                        [
                            66.22733545253872,
                            "#b30000"
                        ],
                        [
                            71.07409766004426,
                            "#7f0000"
                        ]
                    ]
                },
                "fill-opacity": 0.5
            },
            source: "vulnerable_pct",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "COVID vulnerable (comorbidity %)",
        ref: "data/covid_vulnerable.geojson",
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
                            17.47308719988512,
                            "#fee8c8"
                        ],
                        [
                            20.85165637977024,
                            "#fdd49e"
                        ],
                        [
                            24.23022555965536,
                            "#fdbb84"
                        ],
                        [
                            27.60879473954048,
                            "#fc8d59"
                        ],
                        [
                            30.987363919425597,
                            "#ef6548"
                        ],
                        [
                            34.365933099310716,
                            "#d7301f"
                        ],
                        [
                            37.744502279195835,
                            "#b30000"
                        ],
                        [
                            41.123071459080954,
                            "#7f0000"
                        ]
                    ]
                },
                "fill-opacity": 0.5
            },
            source: "pop_elderly",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Elderly population (% over 65)",
        ref: "data/covid_vulnerable.geojson",
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
                            570.6906474517738,
                            "#fde0dd"
                        ],
                        [
                            1115.7812949035474,
                            "#fcc5c0"
                        ],
                        [
                            1660.8719423553212,
                            "#fa9fb5"
                        ],
                        [
                            2205.962589807095,
                            "#f768a1"
                        ],
                        [
                            2751.0532372588686,
                            "#dd3497"
                        ],
                        [
                            3296.1438847106424,
                            "#ae017e"
                        ],
                        [
                            3841.234532162416,
                            "#7a0177"
                        ],
                        [
                            4386.32517961419,
                            "#49006a"
                        ]
                    ]
                },
                "fill-opacity": 0.25
            },
            source: "pop_density",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Population density",
        ref: "data/covid_vulnerable.geojson",
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
            id: "WIMD_rank",
            paint: {
                "fill-color": {
                    property: "WIMD_rank",
                    stops: [
                        [
                            1.0,
                            "#fff7f3"
                        ],
                        [
                            552.2251506114962,
                            "#fde0dd"
                        ],
                        [
                            1103.4503012229925,
                            "#fcc5c0"
                        ],
                        [
                            1654.6754518344887,
                            "#fa9fb5"
                        ],
                        [
                            2205.900602445985,
                            "#f768a1"
                        ],
                        [
                            2757.1257530574812,
                            "#dd3497"
                        ],
                        [
                            3308.3509036689775,
                            "#ae017e"
                        ],
                        [
                            3859.5760542804737,
                            "#7a0177"
                        ],
                        [
                            4410.80120489197,
                            "#49006a"
                        ]
                    ]
                },
                "fill-opacity": 0.25
            },
            source: "WIMD_rank",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Multiple deprivation",
        ref: "data/demos_LSOA.geojson",
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
            id: "internetUse_none_%",
            paint: {
                "fill-color": {
                    property: "internetUse_none_%",
                    stops: [
                        [
                            6.0,
                            "#fff7f3"
                        ],
                        [
                            8.919185677829525,
                            "#fde0dd"
                        ],
                        [
                            11.83837135565905,
                            "#fcc5c0"
                        ],
                        [
                            14.757557033488574,
                            "#fa9fb5"
                        ],
                        [
                            17.6767427113181,
                            "#f768a1"
                        ],
                        [
                            20.595928389147623,
                            "#dd3497"
                        ],
                        [
                            23.515114066977148,
                            "#ae017e"
                        ],
                        [
                            26.434299744806673,
                            "#7a0177"
                        ],
                        [
                            29.353485422636197,
                            "#49006a"
                        ]
                    ]
                },
                "fill-opacity": 0.25
            },
            source: "internetUse_none_%",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "No internet use",
        ref: "data/internetUse.geojson",
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
            id: "internetUse_severalTimesDaily_%",
            paint: {
                "fill-color": {
                    property: "internetUse_severalTimesDaily_%",
                    stops: [
                        [
                            54.0,
                            "#fff7f3"
                        ],
                        [
                            61.11075035159937,
                            "#fde0dd"
                        ],
                        [
                            68.22150070319874,
                            "#fcc5c0"
                        ],
                        [
                            75.3322510547981,
                            "#fa9fb5"
                        ],
                        [
                            82.44300140639749,
                            "#f768a1"
                        ],
                        [
                            89.55375175799685,
                            "#dd3497"
                        ],
                        [
                            96.66450210959621,
                            "#ae017e"
                        ],
                        [
                            103.77525246119558,
                            "#7a0177"
                        ],
                        [
                            110.88600281279496,
                            "#49006a"
                        ]
                    ]
                },
                "fill-opacity": 0.25
            },
            source: "internetUse_severalTimesDaily_%",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Frequent daily internet use",
        ref: "data/internetUse.geojson",
        shownByDefault: false,
        "category": "Demographics",
        "colorsReversed": false,
        "displayOrder": 2
    }
]