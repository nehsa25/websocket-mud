import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AiImageComponent } from './ai-image.component';

describe('AiImageComponent', () => {
  let component: AiImageComponent;
  let fixture: ComponentFixture<AiImageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AiImageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AiImageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
