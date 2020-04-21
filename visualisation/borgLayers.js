var layers=[
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
            id: "groupCount",
            paint: {
                "fill-color": {
                    property: "groupCount",
                    stops: [
                        [
                            0.0,
                            "#ffffe5"
                        ],
                        [
                            0.3923357763560534,
                            "#f7fcb9"
                        ],
                        [
                            0.7846715527121068,
                            "#d9f0a3"
                        ],
                        [
                            1.1770073290681602,
                            "#addd8e"
                        ],
                        [
                            1.5693431054242135,
                            "#78c679"
                        ],
                        [
                            1.9616788817802668,
                            "#41ab5d"
                        ],
                        [
                            2.3540146581363204,
                            "#238443"
                        ],
                        [
                            2.7463504344923737,
                            "#006837"
                        ],
                        [
                            3.138686210848427,
                            "#004529"
                        ]
                    ]
                },
                "fill-opacity": 0.25
            },
            source: "groupCount",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Community support groups",
        ref: "../data/groupCount.geojson",
        shownByDefault: false,
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
                            141.0290683809469,
                            "#fee8c8"
                        ],
                        [
                            239.55813676189385,
                            "#fdd49e"
                        ],
                        [
                            338.0872051428408,
                            "#fdbb84"
                        ],
                        [
                            436.6162735237877,
                            "#fc8d59"
                        ],
                        [
                            535.1453419047346,
                            "#ef6548"
                        ],
                        [
                            633.6744102856816,
                            "#d7301f"
                        ],
                        [
                            732.2034786666285,
                            "#b30000"
                        ],
                        [
                            830.7325470475754,
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
                            552.8433537308575,
                            "#fde0dd"
                        ],
                        [
                            1104.686707461715,
                            "#fcc5c0"
                        ],
                        [
                            1656.5300611925727,
                            "#fa9fb5"
                        ],
                        [
                            2208.37341492343,
                            "#f768a1"
                        ],
                        [
                            2760.2167686542875,
                            "#dd3497"
                        ],
                        [
                            3312.0601223851454,
                            "#ae017e"
                        ],
                        [
                            3863.903476116003,
                            "#7a0177"
                        ],
                        [
                            4415.74682984686,
                            "#49006a"
                        ]
                    ]
                },
                "fill-opacity": 0.5
            },
            source: "WIMD_rank",
            type: "fill",
            "ID_name": "areaID"
        },
        name: "Multiple deprivation",
        ref: "../data/demos_LSOA.geojson",
        shownByDefault: false,
        "category": "Demographics",
        "colorsReversed": false,
        "displayOrder": 2
    }
]