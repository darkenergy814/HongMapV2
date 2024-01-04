import React, {useState} from "react";
import styled from "styled-components";
import {RecommendHandler} from "../../handler/handler";
import {SelectList} from "./selectList";

export function SelectBox(props:any){
    const [input, setInput] = useState<string>('')
    const [select, setSelect] = useState<any>([])
    const handleRecommend = (e: React.ChangeEvent<HTMLInputElement>): void => {
        setInput(e.target.value);
        props.getValue(e.target.value);
        RecommendHandler(e.target.value)
            .then((recommendations) => {
                console.log(recommendations)
                setSelect(recommendations)})
            .catch((error) => console.error('Recommendation request failed:', error.message));
    };

    const handleSelect = (selectedWord: string): void => {
        setInput(selectedWord);
        props.getValue(selectedWord);
        setSelect([]);
        // Additional logic if needed
    };

    return(
        <InputBoxArea>
            <InputBox value={input} type="text" placeholder={props.placeholder} onChange={handleRecommend} />
            {select.length > 0 && <SelectList select={select} onSelect={handleSelect}/>}
        </InputBoxArea>
    );
}

const InputBox = styled.input`
  position: relative;
  width: 297px;
  height: 55px;
  border: none;
  border-radius: 16px;
  color: #000000;
  &::placeholder {
    color: #BCBCBC;
  }
  font-size: medium;
  background-color: #F3F4FF;
  text-align: center;
`

const InputBoxArea = styled.div`
  width: 297px;
`
