import React from "react";
import styled from "styled-components";

export function SelectList(props:  {select: string[]; onSelect: (selectedWord: string) => void}) {
    const select = props.select;
    return (
        <SelectArea>
            {select.map((word:string, index:number) => (
                <RecommendWord key={index} onClick={() => props.onSelect(word)}>{word}</RecommendWord>
            ))}
        </SelectArea>)
}

const SelectArea = styled.div`
  position: relative;
  top: -13px;
  width: 301px;
  max-height: 300px;
  border-bottom-left-radius: 16px;
  border-bottom-right-radius: 16px;
  z-index: 1;
  background-color: #F3F4FF;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: auto;
  
  &::-webkit-scrollbar {
    width: 15px;
  }

  &::-webkit-scrollbar-thumb {
    background-color: #888;
  }
`
const RecommendWord = styled.div`
  position: relative;
  margin: 3px;
  width: 195px;
  height: 31px;
  background: rgba(0, 0, 0, 0);
  color: #000000;
  cursor: pointer;
  text-align: center;
  font-weight: 500;
  line-height: 31px;
  letter-spacing: 0.08px;
`