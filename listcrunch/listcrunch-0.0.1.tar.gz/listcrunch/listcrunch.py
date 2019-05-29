import collections

def crunch(items):
    cruncher = collections.defaultdict(list)
    for num, item in enumerate(items):
        cruncher[item].append(num)
    
    parts = []
    for value in cruncher:
        nums = sorted(cruncher[value])

        subparts = []
        run = None

        def end_run(run):
            if run is None:
                return
            if run[0] == run[1]:
                subparts.append(f"{run[0]}")
            else:
                subparts.append(f"{run[0]}-{run[1]}")
        
        for num in nums:
            if run is None:
                run = [num, num]
            else:
                if num == run[1] + 1:
                    run[1] = num
                else:
                    end_run(run)
                    # Start a new run
                    run = [num, num]

        end_run(run)
        joined = ",".join(subparts)
        parts.append(f"{value}:{joined}")

    return ";".join(parts)

def uncrunch(s):
    if len(s.strip()) == 0: return []

    results = []

    parts = s.split(';')
    for part in parts:
        subparts = part.split(':')
        assert len(subparts) == 2
        value = float(subparts[0])
        specs = subparts[1].split(',')

        for spec in specs:
            if '-' in spec:
                # Parse a range
                startEnd = spec.split('-')
                assert len(startEnd) == 2
                start = int(startEnd[0])
                end = int(startEnd[1])
                for i in range(start, end + 1):
                    results.append([i, value])
            else:
                results.append([int(spec), value])
    
    sorted_results = sorted(results, key=lambda x: x[0])
    nums, values = zip(*sorted_results)
    assert list(nums) == list(range(len(results)))
    return list(values)