test = {
  'name': 'Check hw2.pcap exists',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> assert "hw2.pcap" in os.listdir(".")
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': False,
      'setup': r"""
      >>> import os
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
