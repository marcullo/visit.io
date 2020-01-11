STEPS = """
  [
    {
      "type": "start",
      "location": [
        21.002669,
        52.229069
      ],
      "arrival": 129356,
      "duration": 0
    },
    {
      "type": "job",
      "location": [
        21.015173,
        52.2224751
      ],
      "job": 1,
      "service": 3600,
      "waiting_time": 0,
      "arrival": 129600,
      "duration": 244
    },
    {
      "type": "job",
      "location": [
        21.016066,
        52.2212657
      ],
      "job": 0,
      "service": 3600,
      "waiting_time": 0,
      "arrival": 133297,
      "duration": 341
    },
    {
      "type": "job",
      "location": [
        21.0235775,
        52.2276895
      ],
      "job": 3,
      "service": 1200,
      "waiting_time": 0,
      "arrival": 137079,
      "duration": 523
    },
    {
      "type": "job",
      "location": [
        21.0152518,
        52.2248972
      ],
      "job": 2,
      "service": 2400,
      "waiting_time": 0,
      "arrival": 138406,
      "duration": 650
    },
    {
      "type": "end",
      "location": [
        21.002669,
        52.229069
      ],
      "arrival": 140982,
      "duration": 826
    }
  ]
""".strip()

OPTIMIZATION = """
{
  "code": 0,
  "summary": {
    "cost": 826,
    "unassigned": 0,
    "service": 10800,
    "duration": 826,
    "waiting_time": 0,
    "computing_times": {
      "loading": 1671,
      "solving": 1
    }
  },
  "unassigned": [],
  "routes": [
    {
      "vehicle": 0,
      "cost": 826,
      "service": 10800,
      "duration": 826,
      "waiting_time": 0,
      "steps": [
        {
          "type": "start",
          "location": [
            21.002669,
            52.229069
          ],
          "arrival": 129356,
          "duration": 0
        },
        {
          "type": "job",
          "location": [
            21.015173,
            52.2224751
          ],
          "job": 1,
          "service": 3600,
          "waiting_time": 0,
          "arrival": 129600,
          "duration": 244
        },
        {
          "type": "job",
          "location": [
            21.016066,
            52.2212657
          ],
          "job": 0,
          "service": 3600,
          "waiting_time": 0,
          "arrival": 133297,
          "duration": 341
        },
        {
          "type": "job",
          "location": [
            21.0235775,
            52.2276895
          ],
          "job": 3,
          "service": 1200,
          "waiting_time": 0,
          "arrival": 137079,
          "duration": 523
        },
        {
          "type": "job",
          "location": [
            21.0152518,
            52.2248972
          ],
          "job": 2,
          "service": 2400,
          "waiting_time": 0,
          "arrival": 138406,
          "duration": 650
        },
        {
          "type": "end",
          "location": [
            21.002669,
            52.229069
          ],
          "arrival": 140982,
          "duration": 826
        }
      ]
    }
  ]
}
""".strip()
