python 語音辨識購物助理
===
在我們開始前...
---
請先下載
```
pip install speech_recognition
pip install pyttsx3
```
並使用python 3.10

好了嗎?  
出發:D

如何使用語音系統
---
1. 執行 *shopping_assistant.py* (檔案在專案根目錄)
2. 對你的麥克風說話
    - 沒偵測到聲音會輸出```say something```
      
3. 程式會輸出你講的話、以及分析結果  
    - 例如我講：*關閉程式*  
        ```
        關閉程式
        [('%close%', 1.0)]
        ```
        >第一行是你講的話  
        >第二行是這句話的分析結果
        >1.0為正確率，在0-1之間
    - 也有可能有多個結果，例如我講：*計算如何關閉程式*
        ```
        計算如何關閉程式
        [('%close%', 0.5732758620689655), ('%calculate%', 0.27586206896551724), ('%donothing%', 0.15086206896551727)]
        ```
        >在沒有意義的句子最容易發生  
        >通常模型有訓練好基本上不會發生  
4. 各種動作  
    >有*代表輸入需嚴格遵循格式  
    >其餘則不需要
    - 自我介紹
        1. 介紹自己
            - 範例：你是誰、介紹一下你自己
                >會輸出有關自己的資訊
    - 購物相關
        1. 新增商品至購物車*
            - 格式：加入 *{數量}{量詞}{價錢}* 元的 *{商品名稱}*
                >每個部份均不可少， "加入" 可以用 "新增" 替換
            - 範例：加入3瓶100元的香水、新增6罐5元的麥茶
                >假如新增一個商品，商品名稱和價錢與購物車內某個商品完全相同，則會將數量加在原本商品上面  
                >>例如：購物車已有6罐5元的麥茶，這時輸入 *"新增3罐5元的麥茶"* ，則會將原本購物車內的麥茶加上3罐，變為9罐5元的麥茶

                >假如新增一個商品，商品名稱與購物車內某個商品完全相同，但價錢不相同，這時會把此商品紀錄在此商品名稱之下，而這商品名稱下就有兩種不同價格的商品
                >>例如：購物車內已有3瓶100元的香水，這時輸入 *加入6瓶50元的香水* ，購物車中的 *'香水'* 欄位下就會有兩個商品，一個是100元的香水(3瓶)，另一個則是50元的香水(6瓶)

                >如有設定預算，當某次新增動作會致使總價格超過預算，動作會被拒絕，並輸出 *超過預算:{預算數值}*

        2. 刪除購物車中的特定商品*
            - 格式：刪除 *{商品名稱}*
                >"刪除" 可以用 "移除" 、 "我不要" 替換
            - 範例：刪除巧克力、移除香蕉

        3. 計算購物車中物品價錢總和
            - 範例：商品價錢總和是多少、價錢總和

        4. 刪除購物車中所有物品
            - 範例：清空購物車

        5. 以總價進行折扣
            - 範例：總價打五折
                >如輸入內沒有數字將會報錯，報錯後折扣將被自動重置回1.0
            - 如何取消折扣：輸入 "設定折扣" ，報錯後會自動重置
        
        6. 查詢特定商品花了多少錢*
            - 格式： *{商品名稱}* 花了多少錢
            - 範例：巧克力花了多少錢

        7. 查詢折扣後的價格
            - 範例：最終價格是多少、折後價格是多少

        8. 設定預算
            - 範例：預算800元
                >如果設定預算時，當前總金額超過設定的預算值，將會報錯

        9. 在終端機列出購買的所有品項
            - 範例：列出購物車內的商品、列出購物車

    - 其他
        1. 關閉程式
            - 範例：關閉程式、請你離開、再見、滾吧

        2. 呼叫助理
            - 範例：欸欸欸、你好、我需要你的幫忙

        3. 髒話偵測
            - 你對他說髒話他會說你很兇:D

        4. 其餘辨別不出來的，或是相關性低於50%者，一律回答聽不懂，不執行任何動作

測試系統
---
為了不用每次測試都需要講話，特別增加了這個酷東東  
基本上跟上面的語音系統差不多，只是這是使用打字輸入
1. 執行 *test.py* (檔案在專案跟目錄)
2. 輸入文字
3. 程式會進行輸出，跟語音系統的一樣，在此不多贅述

指令分析模型
---
基本上，我們要讓模型認得指令，就需要先訓練  
那訓練的方法很簡單
1. 找到 *source/text_analyzing/training/training.dat*
2. 在*training.dat*內輸入訓練資料，格式如下  
    ```{字串} %{預期指令名稱}%```  
    >切記 ***{字串}*** 和 ***%{預期指令名稱}%*** 中間要有空格  
    >數字使用阿拉伯數字，不要使用中文數字  
    >除了數字和%%內其他地方全部都是中文
    - 例如：  
        ```
        關閉程式 %close%
        終止操作 %close%
        欸欸欸 %call%
        馬的貢丸 %swear%
        你是茶碗蒸 %swear%
        有時候，風都會穿著小丑服出現 %donothing%
        ```
    - 目前已有指令： 


        | 指令 | 用途 | 範例字串 |
        | :----: | :----: | :----: |
        | %introduce% | 介紹自己 | 介紹一下你自己 |
        | %close% | 關閉程式 | 關閉程式、請你離開 |
        | %call% | 呼叫助理 | 嘿老哥、欸欸欸 |
        | %swear% | 當偵測到輸入髒話時輸出 | ~~就你想得到的髒話~~ |
        | %donothing% | 輸入資料與本程式的功能毫無相關時輸出 | 有時候，風都會穿著小丑服出現 |
        | %add_to_cart% | 將物品新增至購物車 | 加入3瓶100元的香水
        | %remove_from_cart% | 將物品從購物車中刪除 | 刪除巧克力 |
        | %sum_price% | 計算購物車中物品價格總和 | 幫我計算總價錢 |
        | %clear_cart% | 清空購物車 | 刪除購物車的內容 |
        | %discount% | 總價進行折價 | 總價幫我打8折 |
        | %get_info% | 輸出特定商品的價格及數量 | 巧克力花了多少錢 |
        | %final_price% | 計算最終價格(包含折扣後) | 我總共需要付多少錢 |
        | %set_budget% | 限制預算 | 我這次預算是500元 |
        | %list_commodity% | 列出目前購買的所有品項 | 我購物車內有甚麼東西 |

        >為什麼需要 *%donothing%*，感覺有點多此一舉？  
        >舉個例子：
        >>我們這幾個指令中，有四個跟數字有關  
        >>所以存在這種可能，只要輸入的字串中有數字，程式就會在四個指令中擇其一輸出  
        >>但是萬一今天輸入是  
        >>```py
        >>test = '我今天做了10下伏地挺身'
        >>```
        >>這句話跟我們四個指令完全沒關係吧  
        >>但因為這句話裡面有數字，所以和那四個指令相關性特別大而容易造成誤判  
        >>所以才另外加了一個分類去處理和功能相關性不大的句子

3. 執行 *training.py* (檔案在專案根目錄)
    - 執行期間，程式會挨個測試 *training.dat* 內的所有資料  
    資料會先被單獨測試，看結果是否符合預期  
    - 假設一資料為 *媽的貢丸 %swear%* 如果執行結果：
        1. 符合預期，就不會進行訓練，輸出：  
            ```
            #1 module answer is %swear% 1.0, target is %swear%
            command: 媽的貢丸 %swear%
            I've learned this
            ```
            >module answer 是 "媽的貢丸" 輸入模型後得到的結果  
            >target 是預期得到的結果  
            >兩個結果相符，模型已經認得該句子，不會再為其進行訓練

        2. 不符合預期，則會進行訓練：
            ```
            #1 module answer is None None, target is %swear%
            command: 媽的貢丸 %swear%
            failed, I thought it is []
            start training...
            #1 mining start
            Settings:
                    data file: E:\\projects\\SpeechRecognitionAssistant\\source\\text_analyzing\\training\\module_data.dat
                    minimum support: 0.0
                    minimum confidence: 0.8
                    limit: 5
                    write file: True
                    parallel processing: auto
            Times:
            frequency item set:  0.0 sec
            assciation rules:  0.0 sec
            overall time:  0.00049591064453125 sec
            find association rules: 16
            #1 mining end
            done :D
            ```
            >訓練完它就認得了(通常來說)

    - 結束後會有一串輸出  
        ```
        learn 0 statement, fail 0 statement from 16
        ```
        >第一個數字為這次訓練學到多少  
        >第二個是失敗多少，失敗的資料會顯示在下一行，代表這些資料模型學不進去，可能需要換一種表達方式(?)  
        >第三個是總共有多少資料

    - 訓練好的模型會以.json的形式存在 *source/text_analyzing/module_temp/association_rule_module.json* 內

    - 被採用的訓練資料在 *source/text_analyzing/training/module_data.dat* 內  
    於 *association_rule_module.json* 內容損壞時重新訓練用，不要隨意修改

4. 訓練完成後就可以刪掉 *training.py* 內的資料，並新增新的訓練資料

5. 在 *training.py* 有個變數test，可以設定要測試的輸出  
最後會輸出模型所給出的輸出
    - 例如：   
        ```py
        test = '馬的貢丸'
        ```  
        程式輸出：  
        ```
        ('%swear%', 1.0)
        ```
          
        我們就知道模型學會 *馬的貢丸* 了，可喜可賀

