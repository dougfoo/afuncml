def longestPalindrome(s, debug=False):
    """
    :type s: str
    :rtype: str
    """
    maxstr = ""
    curstr = ""

    if (s == len(s) * s[0]):
        return s

    for i in range(len(s)):
        prev = i-1 
        next = i+1
        curstr = s[i]
        while (prev >=0 and next < len(s)):
            if (debug == True):
                print(prev,i,next,curstr,s)
            if (1==5):
                pass
            elif (s[prev] == s[next]):
                curstr = s[prev] + curstr + s[next]
                if (debug == True):
                    print('match',prev,i,next,'['+curstr+']',s) 
                next = next+1
                prev = prev-1
            # need to check if its a palmatch
            elif (s[next] == s[next-1] and curstr == len(curstr) * curstr[0]):
                curstr = curstr + s[next]
                next = next+1
            elif (s[prev] == s[prev+1] and curstr == len(curstr) * curstr[0]):
                curstr = s[prev] + curstr 
                prev = prev-1
            else:
                break

        maxstr = curstr if len(curstr) > len(maxstr) else maxstr            
#    print('  ',maxstr,s)                    
    return maxstr

tests = [
    ["a","a"],
    ["aa","aa"],
    ["bbb","bbb"],
    ["cccc","cccc"],
    ["abccbde","bccb"],
    ["babad","bab"],
    ["cbbd","bb"],
    ["bananas","anana"],
    ["aaabaaaa","aaabaaa"],
    ["xaaay","aaa"],
    ["cbb","bb"],
    ["aab","aa"],
    ["222020221","2202022"],
]

for t in tests:
    r = longestPalindrome(t[0])
    if (r != t[1]):
        print('**Fail Start**',r,'!=', t)
        longestPalindrome(t[0], True)
        print('**Fail End**',r,'!=', t)
